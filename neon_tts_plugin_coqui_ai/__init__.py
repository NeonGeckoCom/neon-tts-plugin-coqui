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

from typing import Optional
from neon_utils.configuration_utils import get_neon_tts_config
from neon_utils.logger import LOG
from neon_utils.parse_utils import format_speak_tags

try:
    from neon_audio.tts import TTS, TTSValidator
except ImportError:
    from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from neon_utils.metrics_utils import Stopwatch

from huggingface_hub import snapshot_download

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


class CoquiTTS(TTS):
    langs = {
        "en": {
            "model": "tts_models/en/ljspeech/vits", 
            "vocoder": None
        },
        "pl": {
            "model": "NeonBohdan/tts-glow-mai-pl", 
            "vocoder": "vocoder_models/en/ljspeech/hifigan_v2"
        }
    }

    def __init__(self, lang="en", config=None):
        config = config or get_neon_tts_config().get("coqui", {})
        super(CoquiTTS, self).__init__(lang, config, CoquiTTSValidator(self),
                                          audio_ext="wav",
                                          ssml_tags=["speak"])
        self.engines = {}
        self.manager = ModelManager()
        self.cache_engines = config.get("cache", True)

    def get_tts(self, sentence: str, output_file: str, speaker: Optional[dict] = None):
        stopwatch = Stopwatch()
        speaker = speaker or dict()

        # TODO: speaker params are optionally defined and should be handled whenever defined
        # # Read utterance data from passed configuration
        # request_lang = speaker.get("language",  self.lang)
        # request_gender = speaker.get("gender", "female")
        # request_voice = speaker.get("voice")

        request_lang = speaker.get("language",  self.lang).split('-')[0]
        synthesizer = self._init_model(request_lang)

        to_speak = format_speak_tags(sentence)
        LOG.debug(to_speak)
        if to_speak:
            with stopwatch:
                wav_data = synthesizer.tts(sentence)
            LOG.debug(f"TTS Synthesis time={stopwatch.time}")

            with stopwatch:
                synthesizer.save_wav(wav_data, output_file)
            LOG.debug(f"File access time={stopwatch.time}")

        return output_file, None

    def _init_model(self, lang):
        lang_params = self.langs[lang]
        model_name = lang_params["model"]
        vocoder_name = lang_params["vocoder"]

        model_path, config_path = self._download_model(model_name)
        vocoder_path, vocoder_config_path = self._download_model(vocoder_name)

        # create synthesizer
        if lang not in self.engines:
            synt = Synthesizer(tts_checkpoint=model_path,
                               tts_config_path=config_path,
                               vocoder_checkpoint=vocoder_path,
                               vocoder_config=vocoder_config_path)
            if self.cache_engines:
                self.engines[lang] = synt
        else:
            synt = self.engines[lang]
        return synt

    def _download_model(self, model_name):
        if model_name is None:
            return None, None
            
        prefix = model_name.split("/")[0]
        if (prefix == "tts_models") or (prefix == "vocoder_models"):
            model_path, config_path = self._download_coqui(model_name)
        else:
            model_path, config_path = self._download_huggingface(model_name)

        return model_path, config_path

    def _download_coqui(self, model_name):
        model_path, config_path, _ = self.manager.download_model(model_name)
        return model_path, config_path

    def _download_huggingface(self, model_name):
        repo_path = snapshot_download(model_name)

        model_path = repo_path + "/model_file.pth.tar"
        config_path = repo_path + "/config.json"

        self.manager._update_paths(repo_path, config_path)
        
        return model_path, config_path

class CoquiTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CoquiTTSValidator, self).__init__(tts)

    def validate_lang(self):
        if (self.tts.lang not in CoquiTTS.langs):
            raise KeyError("Language isn't supported")

    def validate_dependencies(self):
        # TODO: Optionally check dependencies or raise
        pass

    def validate_connection(self):
        # TODO: Optionally check connection to remote service or raise
        pass

    def get_tts_class(self):
        return CoquiTTS
