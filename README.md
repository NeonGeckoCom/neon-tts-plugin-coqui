# NeonAI Coqui AI TTS Plugin
[Mycroft](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins) compatible
TTS Plugin for Coqui AI Text-to-Speech.

# Languages:
We support all European Union languages such as:

English, Spanish, French, German, Italian, Polish, Ukrainian, \
Dutch, Romanian, Hungarian, Greek, Czech, Swedish, Portuguese, \
Croatian, Bulgarian, Danish, Slovak, Finnish, Lithuanian, \
Slovenian, Latvian, Estonian, Irish, Maltese

Feel free to open an issue to request support of your language. We implement the languages we want and not the ones we can.\
So even Irish and Maltese are not a problem even though they have less than a million native speakers.

# Configuration:
```yaml
tts:
    module: coqui
    coqui: {
        cache: true
    }
```
# Requirements:
`sudo apt install espeak-ng`

Necessary for english, greek and some other languages

## Docker

A docker container using [ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) is available

You can build and run it locally

```bash
docker build . -t coquitts
docker run -p 8080:9666 coquitts
```

use it `http://localhost:8080/synthesize/hello`
