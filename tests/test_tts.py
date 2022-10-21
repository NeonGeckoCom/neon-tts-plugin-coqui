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
from speechbrain.pretrained import EncoderClassifier

# sys.path.append(os.path.join(os.path.dirname(__file__), "res"))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from neon_tts_plugin_coqui import CoquiTTS


class TestTTS(unittest.TestCase):
    lang_exeptions = {
        "ga": "en",
        "es": "gl,eu,es", #TODO: Spain sub-languages
        "sv": "nn,sv",
        "hr": "bs,hr",
        "pt": "bg,pt"
    }

    @classmethod
    def setUpClass(TestTTS):
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning) 
        # language detector
        TestTTS.init_lang_detector()

    @classmethod
    def init_lang_detector(TestTTS):
        download_path = os.path.expanduser("~")+"/.cache/huggingface/hub/lang_detector"
        model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa",
                                                savedir=download_path)
        TestTTS.lang_detector = {
            "model": model,
            "sr": 16000
        }

    def detect_language(self, wav_data: list, synthesizer: object):
        wav_numpy = np.array(wav_data)
        wav_low = resampy.resample(wav_numpy, synthesizer.tts_model.ap.sample_rate, self.lang_detector["sr"])
        wav_tensor = torch.tensor(wav_low, dtype=torch.float32)
        prediction = self.lang_detector["model"].classify_batch(wav_tensor)
        language = prediction[3][0]
        score = prediction[1][0].exp()
        print(f'Language: {language} with prob {score:.2f}')
        lang_code = language.split(":")[0]
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
                if (lang in self.lang_exeptions):
                    lang_exeption = self.lang_exeptions[lang]
                    print(f"Language {lang} is an exeption and detected as {lang_exeption}")
                    lang = lang_exeption
                self.assertIn(detected_language, lang)

    def test_ipython_format(self):
        ipython_dict = self.tts.get_audio("Hello.", audio_format="ipython")
        self.assertIsInstance(ipython_dict, dict)
        self.assertTrue({"data", "rate"} <= {*ipython_dict})
        self.assertIsInstance(ipython_dict["data"], list)

    def test_available_languages(self):
        from neon_tts_plugin_coqui.configs import languages
        supported_langs = set(languages.keys())
        self.assertEqual(self.tts.available_languages, supported_langs)


class TestConfigs(unittest.TestCase):
    def test_languages(self):
        from neon_tts_plugin_coqui.configs import languages
        self.assertIsInstance(languages, dict)
        for lang in languages:
            self.assertEqual(set(languages[lang].keys()),
                             {'model', 'language', 'sentence'})
            self.assertIsInstance(languages[lang]['model'], str)
            self.assertIsInstance(languages[lang]['language'], dict)
            self.assertIsInstance(languages[lang]['sentence'], str)

    def test_tts_config(self):
        from neon_tts_plugin_coqui.configs import languages, tts_config
        self.assertEqual(len(languages), len(tts_config))
        for lang, configs in tts_config.items():
            self.assertIsInstance(configs, list)
            for config in configs:
                self.assertEqual(config['lang'], lang)
                self.assertIsInstance(config['display_name'], str)
                self.assertTrue(config['offline'])


if __name__ == '__main__':
    unittest.main()
