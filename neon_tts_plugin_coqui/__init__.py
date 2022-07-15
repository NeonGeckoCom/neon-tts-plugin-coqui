# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import psutil
import ctypes
import gc

from typing import Optional
from ovos_utils.log import LOG
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils.metrics import Stopwatch
from huggingface_hub import hf_hub_download
from torch import no_grad, package

from .configs import languages


class CoquiTTS(TTS):
    proc = psutil.Process(os.getpid())

    langs = languages

    def _get_mem_usage(self) -> str:
        """
        Get the current process memory usage in MiB
        Returns: str memory usage in MiB
        """
        return self.proc.memory_info().rss / 1048576  # b to MiB

    def __init__(self, lang="en", config=None, *args, **kwargs):
        super(CoquiTTS, self).__init__(lang, config, CoquiTTSValidator(self),
                                       audio_ext="wav",
                                       ssml_tags=["speak"])
        self.engines = {}
        self.cache_engines = self.config.get("cache", True)
        if self.cache_engines:
            self._init_model({"lang": lang})

    def get_tts(self, sentence: str, output_file: str,
                speaker: Optional[dict] = None) -> (str, Optional[str]):
        """
        Get Synthesized audio
        Args:
            sentence: string to synthesize
            output_file: path to output audio file
            speaker: optional dict speaker data

        Returns:
            tuple wav_file, optional phonemes
        """
        wav_data, synthesizer = self.get_audio(sentence, speaker,
                                               audio_format="internal")
        self._audio_to_file(wav_data, synthesizer, output_file)
        return output_file, None

    def get_audio(self, sentence: str, speaker: Optional[dict] = None,
                  audio_format: str = "internal"):
        """
        Use this method for accessing generated audio in a format convenient for you
        Args:
            sentence: string to synthesize
            speaker: optional dict speaker data
            audio_format: str audio format to return ('internal' or 'ipython')
        Examples:
            Run in IPython Notebook.

            >>> from neon_tts_plugin_coqui import CoquiTTS
            >>> import IPython
            >>> tts = CoquiTTS("uk")
            >>> ipython_dict = tts.get_audio("Привіт хлопче", audio_format="ipython")
            >>> IPython.display.display(IPython.display.Audio(**ipython_dict,  autoplay=True))
        """
        stopwatch = Stopwatch()
        speaker = speaker or dict()

        synthesizer, tts_kwargs = self._init_model(speaker)
        with stopwatch:
            with no_grad():
                wav_data = synthesizer.tts(sentence, **tts_kwargs)
                self._trim_memory()

        LOG.debug(f"TTS Synthesis time={stopwatch.time}")
        LOG.debug(f"RAM={self._get_mem_usage()} MiB")

        if audio_format == "internal":
            return wav_data, synthesizer
        elif audio_format == "ipython":
            return self._audio_to_ipython(wav_data, synthesizer)

    @staticmethod
    def _audio_to_file(wav_data: list, synthesizer: object,
                       output_file: str):
        """
        Write synthesized audio to a file
        Args:
            wav_data: wav_data returned by `synthesizer.tts`
            synthesizer: synthesizer object used to generate `wav_data`
            output_file: output path to write
        """
        stopwatch = Stopwatch()

        with stopwatch:
            synthesizer.save_wav(wav_data, output_file)
        LOG.debug(f"File access time={stopwatch.time}")

    @staticmethod
    def _audio_to_ipython(wav_data: list, synthesizer: object) -> dict:
        """
        Get a dict representation of synthesized audio for IPython display
        Args:
            wav_data: wav_data returned by `synthesizer.tts`
            synthesizer: synthesizer object used to generate `wav_data`

        Returns:
            dict to be displayed with IPython
        """
        ipython_dict = {
            "data": wav_data,
            "rate": synthesizer.output_sample_rate
        }
        return ipython_dict

    @staticmethod
    def _trim_memory():
        """
        If possible, gives memory allocated by PyTorch back to the system
        """
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
        gc.collect()

    def _init_model(self, speaker: dict) -> (object, dict):
        """
        Initialize a synthesizer for the specified speaker
        Args:
            speaker: dict speaker to initialize a model for with keys:
                `language` - language code
                `gender` - optional synthesizer gender requested
                `voice` - optional synthesizer voice requested

        Returns:
            tuple Synthesizer, parsed tts kwargs from `speaker`
        """
        # lang
        lang = speaker.get("language", self.lang).split('-')[0]
        # synthesizer
        if lang not in self.engines:
            LOG.info(f"Initializing model for: {lang}")
            synt = self._init_synthesizer(lang)
            if self.cache_engines:
                self.engines[lang] = synt
        else:
            LOG.debug(f"Using loaded model for: {lang}")
            synt = self.engines[lang]
        # tts kwargs
        tts_kwargs = self._init_tts_kwargs(lang, speaker, synt)
        # log
        LOG.debug(f"RAM={self._get_mem_usage()} MiB")
        return synt, tts_kwargs

    def _init_tts_kwargs(self, lang: str, speaker: dict, synthesizer: object) -> dict:
        """
        Parse language and speaker requests into a valid dict of tts kwargs
        Args:
            lang: 2-letter ISO 639-1 Language code
            speaker: additional optional speaker parameters requested
                `gender` - optional synthesizer gender requested
                `voice` - optional synthesizer voice requested

        Returns:
            parsed tts kwargs to pass to synthesizer init
        """
        # TODO: handle speaker['gender'] here DM
        speaker_name = speaker.get("voice") or lang
        tts_kwargs = {
            "speaker_name": speaker_name,
            "language_name": lang
        }
        # handle multi-speaker
        if not hasattr(synthesizer.tts_model.speaker_manager, "ids"):
            tts_kwargs["speaker_name"] = ""
        # log
        LOG.debug(f"tts_kwargs={tts_kwargs}")
        return tts_kwargs

    def _init_synthesizer(self, lang: str) -> object:
        """
        Create a Synthesizer for the requested language
        Args:
            lang: 2-letter ISO 639-1 Language code
        Returns:
            Synthesizer initialized with a model for the requested `lang`
        """
        # TODO: Handle optional `name` and `gender` model specs
        lang_params = self.langs[lang]
        model_name = lang_params["model"]

        model_path = self._download_huggingface(model_name)

        importer = package.PackageImporter(model_path)
        synt = importer.load_pickle("tts_models", "model")
        return synt

    def _download_huggingface(self, model_name) -> str:
        """
        Download a model from Huggingface
        Args:
            model_name: name of model to download

        Returns:
            tuple model_path, config_path
        """

        # get revision
        model_name, *suffix = model_name.split("@")
        revision = dict(enumerate(suffix)).get(0, None)

        model_path = hf_hub_download(model_name, "model.pt", revision=revision)

        return model_path


class CoquiTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CoquiTTSValidator, self).__init__(tts)

    def validate_lang(self):
        if self.tts.lang.split('-')[0] not in CoquiTTS.langs:
            raise KeyError(f"Language isn't supported: {self.tts.lang}")

    def validate_dependencies(self):
        # TODO: Optionally check dependencies or raise
        pass

    def validate_connection(self):
        # TODO: Optionally check connection to remote service or raise
        pass

    def get_tts_class(self):
        return CoquiTTS
