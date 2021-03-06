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
import sys
import unittest
from pprint import pprint

import resampy
import torch
import numpy as np

# sys.path.append(os.path.join(os.path.dirname(__file__), "res"))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from neon_tts_plugin_coqui import CoquiTTS


class TestTTS(unittest.TestCase):

    @classmethod
    def setUpClass(TestTTS):
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning) 
        # language detector
        TestTTS.init_lang_detector()

    @classmethod
    def init_lang_detector(TestTTS):
        model, lang_dict, lang_group_dict, \
        (get_language_and_group, _) = torch.hub.load(repo_or_dir='NeonGeckoCom/silero-vad:neon-master',
                                                           model='silero_lang_detector_95',
                                                           force_reload=True)
                                                        
        TestTTS.lang_detector = {
            "model": model,
            "lang_dict": lang_dict,
            "lang_group_dict": lang_group_dict,
            "get_language_and_group": get_language_and_group,
            "sr": 16000
        }

    def detect_language(self, wav_data: list, synthesizer: object):
        wav_numpy = np.array(wav_data)
        wav_low = resampy.resample(wav_numpy, synthesizer.tts_model.ap.sample_rate, self.lang_detector["sr"])
        wav_tensor = torch.tensor(wav_low, dtype=torch.float32)
        languages, _ = self.lang_detector["get_language_and_group"](wav_tensor, self.lang_detector["model"], 
                            self.lang_detector["lang_dict"], self.lang_detector["lang_group_dict"], top_n=2)
        language = languages[0]
        print(f'Language: {language[0]} with prob {language[-1]}')
        lang_code = language[0].split(",")[0]
        return lang_code


    def setUp(self) -> None:
        self.tts = CoquiTTS(config={"cache":False})

    def doCleanups(self) -> None:
        self.deleteFiles()
        try:
            self.tts.playback.stop()
            self.tts.playback.join()
        except (AttributeError, RuntimeError):
            pass

    def deleteFiles(self) -> None:
        try:
            os.remove(os.path.join(os.path.dirname(__file__), "test.wav"))
        except FileNotFoundError:
            pass

    def test_speak_no_params(self):
        out_file = os.path.join(os.path.dirname(__file__), "test.wav")
        file, _ = self.tts.get_tts("Hello.", out_file)
        self.assertEqual(file, out_file)

    def test_speak_lang(self):
        for lang in CoquiTTS.langs:
            sentence = CoquiTTS.langs[lang]["sentence"]
            with self.subTest(lang=lang):
                speaker = {
                    "language" : lang
                }
                wav_data, synthesizer = self.tts.get_audio(sentence, speaker = speaker)
                detected_language = self.detect_language(wav_data, synthesizer)
                self.assertEqual(lang, detected_language)

    def test_ipython_format(self):
        ipython_dict = self.tts.get_audio("Hello.", audio_format="ipython")
        self.assertIsInstance(ipython_dict, dict)
        self.assertTrue({"data", "rate"} <= {*ipython_dict})
        self.assertIsInstance(ipython_dict["data"], list)


if __name__ == '__main__':
    unittest.main()
