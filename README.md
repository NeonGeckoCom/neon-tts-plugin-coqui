# NeonAI Coqui AI TTS Plugin
[Mycroft](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins) compatible
TTS Plugin for Coqui AI Text-to-Speech.

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

Necessary for recording audio files

## Docker

A docker container using [ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) is available

You can build and run it locally

```bash
docker build . -t coquitts
docker run -p 8080:9666 coquitts
```

use it `http://localhost:8080/synthesize/hello`
