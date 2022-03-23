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


class CoquiTTS(TTS):
    def __init__(self, lang="en-us", config=None):
        config = config or get_neon_tts_config().get("coqui", {})
        super(CoquiTTS, self).__init__(lang, config, CoquiTTSValidator(self),
                                          audio_ext="mp3",  # TODO: Specify output audio format
                                          ssml_tags=["speak"])  # TODO: Specify valid SSML tags
        # TODO: Optionally define any class parameters

    def get_tts(self, sentence: str, output_file: str, speaker: Optional[dict] = None):
        stopwatch = Stopwatch()
        speaker = speaker or dict()

        # TODO: speaker params are optionally defined and should be handled whenever defined
        # # Read utterance data from passed configuration
        # request_lang = speaker.get("language",  self.lang)
        # request_gender = speaker.get("gender", "female")
        # request_voice = speaker.get("voice")

        # TODO: Below is an example of a common ambiguous language code; test and implement or remove
        # # Catch Chinese alt code
        # if request_lang.lower() == "zh-zh":
        #     request_lang = "cmn-cn"

        to_speak = format_speak_tags(sentence)
        LOG.debug(to_speak)
        if to_speak:
            with stopwatch:
                pass
                # TODO: Get TTS audio here

            LOG.debug(f"TTS Synthesis time={stopwatch.time}")

        return output_file, None


class CoquiTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CoquiTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO: Add some validation of `self.lang` default language
        pass

    def validate_dependencies(self):
        # TODO: Optionally check dependencies or raise
        pass

    def validate_connection(self):
        # TODO: Optionally check connection to remote service or raise
        pass

    def get_tts_class(self):
        return CoquiTTS
