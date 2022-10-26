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

languages = {
    "en": {
        "model": "neongeckocom/tts-vits-ljspeech-en@v0.4",
        "language": {
            "name": "English (US)",
            "code": "en-US",
            "gender": "female"
        },
        "sentence": "A rainbow is a meteorological phenomenon that is caused "
                    "by reflection, refraction and dispersion of light.",
    },
    "es": {
        "model": "neongeckocom/tts-vits-css10-es@v0.2",
        "language": {
            "name": "Spanish (Spain)",
            "code": "es-ES",
            "gender": "male"
        },
        "sentence": "Un arcoíris o arco iris es un fenómeno óptico y "
                    "meteorológico que consiste en la aparición en el cielo "
                    "de un arco de luz multicolor.",
    },
    "fr": {
        "model": "neongeckocom/tts-vits-css10-fr@v0.3", 
        "sentence": "Un arc-en-ciel est un photométéore, un phénomène optique "
                    "se produisant dans le ciel, visible dans la direction "
                    "opposée au Soleil.",
        "language": {
            "name": "French (France)",
            "code": "fr-FR",
            "gender": "male"
        },
    },
    "de": {
        "model": "neongeckocom/tts-vits-css10-de@v0.2", 
        "sentence": "Der Regenbogen ist ein atmosphärisch-optisches Phänomen, "
                    "das als kreisbogenförmiges farbiges Lichtband in einer "
                    "von der Sonne.",
        "language": {
            "name": "German",
            "code": "de-DE",
            "gender": "female"
        },
    },
    "it": {
        "model": "neongeckocom/tts-vits-cv-it@v0.1",
        "language": {
            "name": "Italian",
            "code": "it-IT",
            "gender": "female"
        },
        "sentence": "In fisica dell'atmosfera e meteorologia, l'arcobaleno è "
                    "un fenomeno ottico atmosferico che produce uno spettro "
                    "quasi continuo di luce nel cielo quando la luce del Sole "
                    "attraversa le gocce d'acqua rimaste in sospensione dopo "
                    "un temporale.",
    },
    "pl": {
        "model": "neongeckocom/tts-vits-mai-pl@v0.6",
        "language": {
            "name": "Polish",
            "code": "pl-PO",
            "gender": "female"
        },
        "sentence": "Tęcza, zjawisko optyczne i meteorologiczne, występujące "
                    "w postaci charakterystycznego wielobarwnego łuku "
                    "powstającego w wyniku rozszczepienia światła widzialnego.",
    },
    "uk": {
        "model": "neongeckocom/tts-vits-mai-uk@v0.9",
        "language": {
            "name": "Ukrainian",
            "code": "uk-UA",
            "gender": "female"
        },
        "sentence": "Веселка, також райдуга оптичне явище в атмосфері, що "
                    "являє собою одну, дві чи декілька різнокольорових дуг, "
                    "що спостерігаються на тлі хмари, якщо вона розташована "
                    "проти Сонця.",
    },
    "nl": {
        "model": "neongeckocom/tts-vits-css10-nl@v0.2",
        "language": {
            "name": "Dutch",
            "code": "nl-NL",
            "gender": "male"
        },
        "sentence": "Een regenboog is een gekleurde cirkelboog die aan de "
                    "hemel waargenomen kan worden als de, laagstaande.",
    },
    "ro": {
        "model": "neongeckocom/tts-vits-cv-ro@v0.1",
        "language": {
            "name": "Romanian",
            "code": "ro-RO",
            "gender": "female"
        },
        "sentence": "Curcubeul este un fenomen optic și meteorologic "
                    "atmosferic care se manifestă prin apariția pe cer a unui "
                    "spectru de forma unui arc colorat atunci când lumina "
                    "soarelui se refractă în picăturile de apă din atmosferă.",
    },
    "hu": {
        "model": "neongeckocom/tts-vits-css10-hu@v0.1",
        "language": {
            "name": "Hungarian",
            "code": "hu-HU",
            "gender": "female"
        },
        "sentence": "A szivárvány olyan optikai jelenség, melyet eső- vagy "
                    "páracseppek okoznak, mikor a fény prizmaszerűen megtörik "
                    "rajtuk és színeire bomlik.",
    },
    "el": {
        "model": "neongeckocom/tts-vits-cv-el@v0.1",
        "language": {
            "name": "Greek",
            "code": "el-GR",
            "gender": "female"
        },
        "sentence": "Το ουράνιο τόξο εμφανίζεται όταν οι ακτίνες του ήλιου "
                    "χτυπούν σταγόνες βροχής στην ατμόσφαιρα της Γης και "
                    "είναι ένα παράδειγμα διάθλασης μετά την ανάκλαση.",
    },
    "cs": {
        "model": "neongeckocom/tts-vits-cv-cs@v0.1",
        "language": {
            "name": "Czech",
            "code": "cs-CZ",
            "gender": "female"
        },
        "sentence": "Duha je fotometeor, projevující se jako skupina "
                    "soustředných barevných oblouků, které vznikají lomem a "
                    "vnitřním odrazem slunečního nebo měsíčního světla na "
                    "vodních kapkách v atmosféře.",
    },
    "sv": {
        "model": "neongeckocom/tts-vits-cv-sv@v0.1",
        "language": {
            "name": "Swedish",
            "code": "sv-SE",
            "gender": "female"
        },
        "sentence": "En regnbåge är ett optiskt, meteorologiskt fenomen som "
                    "uppträder som ett fullständigt ljusspektrum i form av en "
                    "båge på himlen då solen lyser på nedfallande regn. "
                    "Klarast lyser regnbågen då halva himlen fortfarande är "
                    "täckt med mörka moln som avger regn och betraktaren "
                    "befinner sig under klar himmel.",
    },
    "pt": {
        "model": "neongeckocom/tts-vits-cv-pt@v0.1",
        "language": {
            "name": "Portuguese (Portugal)",
            "code": "pt-PT",
            "gender": "male"
        },
        "sentence": "Um arco-íris é um fenômeno óptico e meteorológico que "
                    "separa a luz do sol em seu espectro contínuo quando o "
                    "sol brilha sobre gotículas de água suspensas no ar.",
    },
    "bg": {
        "model": "neongeckocom/tts-vits-cv-bg@v0.1",
        "language": {
            "name": "Bulgarian",
            "code": "bg-BG",
            "gender": "female"
        },
        "sentence": "Дъга е оптично и метеорологично явление, свързано с "
                    "появата в небето на почти непрекъснат спектър на "
                    "светлината.",
    },
    "hr": {
        "model": "neongeckocom/tts-vits-cv-hr@v0.1",
        "language": {
            "name": "Hungarian",
            "code": "hr-HU",
            "gender": "female"
        },
        "sentence": "Duga je česta optička pojava u Zemljinoj atmosferi u "
                    "obliku jednog ili više obojenih kružnih lukova, koja "
                    "nastaje jednostrukim ili višestrukim lomom i odbijanjem "
                    "zraka svjetlosti u kapljicama kiše.",
    },
    "da": {
        "model": "neongeckocom/tts-vits-cv-da@v0.1",
        "language": {
            "name": "Danish",
            "code": "da-DK",
            "gender": "female"
        },
        "sentence": "En regnbue er et optisk fænomen; en lyseffekt, som "
                    "skabes på himlen, når lys fra Solen rammer små "
                    "vanddråber i luften, f.eks. faldende regn.",
    },
    "sk": {
        "model": "neongeckocom/tts-vits-cv-sk@v0.1",
        "language": {
            "name": "Slovak",
            "code": "sk-SK",
            "gender": "female"
        },
        "sentence": "Dúha je optický úkaz vznikajúci v atmosfére Zeme. Vznik "
                    "dúhy je spôsobený disperziou slnečného svetla "
                    "prechádzajúceho kvapkou.",
    },
    "fi": {
        "model": "neongeckocom/tts-vits-css10-fi@v0.1",
        "language": {
            "name": "Finnish",
            "code": "fi-FI",
            "gender": "male"
        },
        "sentence": "Sateenkaari on spektrin väreissä esiintyvä ilmakehän "
                    "optinen ilmiö. Se syntyy, kun valo taittuu pisaran "
                    "etupinnasta.",
    },
    "lt": {
        "model": "neongeckocom/tts-vits-cv-lt@v0.1",
        "language": {
            "name": "Lithuanian",
            "code": "lt-LT",
            "gender": "female"
        },
        "sentence": "Vaivorykštė - optinis ir meteorologinis reiškinys, "
                    "kuomet Saulei apšvietus atmosferoje esančius vandens "
                    "lašelius, danguje atsiranda ištisinė spalvų spektro "
                    "juosta.",
    },
    "sl": {
        "model": "neongeckocom/tts-vits-cv-sl@v0.1",
        "language": {
            "name": "Slovenian",
            "code": "sl-SI",
            "gender": "female"
        },
        "sentence": "Mavrica je svetlobni pojav v ozračju, ki ga vidimo v "
                    "obliki loka spektralnih barv. Nastane zaradi loma, "
                    "disperzije in odboja sončnih žarkov v vodnih kapljicah v "
                    "zraku. Mavrica, ki nastane zaradi sončnih žarkov, se "
                    "vedno pojavi na nasprotni strani od Sonca, tako da ima "
                    "opazovalec Sonce vedno za hrbtom.",
    },
    "lv": {
        "model": "neongeckocom/tts-vits-cv-lv@v0.1",
        "language": {
            "name": "Latvian",
            "code": "lv-LV",
            "gender": "female"
        },
        "sentence": "Varavīksne ir optiska parādība atmosfērā, kuru rada "
                    "Saules staru laušana un atstarošana krītošos lietus "
                    "pilienos. Tā parādās iepretim Saulei uz mākoņu fona, kad "
                    "līst. Varavīksnes loks pāri debesjumam ir viens no "
                    "krāšņākajiem dabas skatiem. Pārējās krāsas izvietojušās "
                    "atbilstoši tā loka gammai.",
    },
    "et": {
        "model": "neongeckocom/tts-vits-cv-et@v0.1",
        "language": {
            "name": "Estonian",
            "code": "et-EE",
            "gender": "female"
        },
        "sentence": "Vikerkaare põhjustab päikesekiirte eri lainepikkustel "
                    "erinev murdumine ja peegeldumine ligikaudu "
                    "kerakujulistelt vihmapiiskadelt vihmaseinal või "
                    "vihmapilves, kui päikesevalgus langeb piiskadele "
                    "vaatleja selja tagant.",
    },
    "ga": {
        "model": "neongeckocom/tts-vits-cv-ga@v0.2",
        "language": {
            "name": "Irish (Gaelic)",
            "code": "ga-IE",
            "gender": "female"
        },
        "sentence": "Do réir lucht na heolaíochta, is é solas na gréine ag "
                    "taitneamh ar bhraonta báistí sa spéir faoi ndearna an "
                    "tuar ceatha. Dar linne ná tagann ón ngréin ach aon "
                    "tsolais amháin, ach ní mar sin atá.",
    },
    "mt": {
        "model": "neongeckocom/tts-vits-cv-mt@v0.1",
        "language": {
            "name": "Maltese",
            "code": "mt-MT",
            "gender": "female"
        },
        "sentence": "Qawsalla hija fenomenu meteoroloġiku li huwa kkawżat "
                    "minn riflessjoni, rifrazzjoni u tixrid ta 'dawl fi qtar "
                    "ta' l-ilma li jirriżulta fi spettru ta 'dawl li jidher "
                    "fis-sema.",
    },
}

tts_config = {config['language']['code']: [
    {
        'lang': config['language']['code'],
        'display_name': f'{config["language"]["name"]}',
        'gender': config["language"]["gender"],
        'offline': True,
        'priority': 20
    }
] for config in languages.values()}
