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

# sys.path.append(os.path.join(os.path.dirname(__file__), "res"))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from neon_tts_plugin_coqui import CoquiTTS


class TestTTS(unittest.TestCase):
    languages = [
        ["en", "A rainbow is a meteorological phenomenon that is caused by reflection, refraction and dispersion of light."],
        ["es", "Un arcoíris o arco iris es un fenómeno óptico y meteorológico que consiste en la aparición en el cielo de un arco de luz multicolor."],
        ["fr", "Un arc-en-ciel est un photométéore, un phénomène optique se produisant dans le ciel, visible dans la direction opposée au Soleil."],
        ["de", "Der Regenbogen ist ein atmosphärisch-optisches Phänomen, das als kreisbogenförmiges farbiges Lichtband in einer von der Sonne."],
        ["pl", "Tęcza, zjawisko optyczne i meteorologiczne, występujące w postaci charakterystycznego wielobarwnego łuku."],
        ["uk", "Веселка, також райдуга оптичне явище в атмосфері, що являє собою одну, дві чи декілька різнокольорових дуг."],
        ["nl", "Een regenboog is een gekleurde cirkelboog die aan de hemel waargenomen kan worden als de, laagstaande."],
        ["fi", "Sateenkaari on spektrin väreissä esiintyvä ilmakehän optinen ilmiö. Se syntyy, kun valo taittuu pisaran etupinnasta."],
    ]

    @classmethod
    def setUpClass(TestTTS):
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning) 


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
        for lang, sentence in self.languages:
            with self.subTest(lang=lang):
                speaker = {
                    "language" : lang
                }
                out_file = os.path.join(os.path.dirname(__file__), "test.wav")
                file, _ = self.tts.get_tts(sentence, out_file, speaker = speaker)
                self.assertEqual(file, out_file)
                self.deleteFiles()

    def test_ipython_format(self):
        out_file = os.path.join(os.path.dirname(__file__), "test.wav")
        ipython_dict = self.tts.get_audio("Hello.", audio_format="ipython")
        self.assertIsInstance(ipython_dict, dict)
        self.assertTrue({"data", "rate"} <= {*ipython_dict})
        self.assertIsInstance(ipython_dict["data"], list)


if __name__ == '__main__':
    unittest.main()
