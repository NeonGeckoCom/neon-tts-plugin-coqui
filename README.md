# NeonAI Coqui AI TTS Plugin
[Mycroft](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins) compatible
TTS Plugin for Coqui AI Text-to-Speech.

# Configuration:
```yaml
tts:
    module: coqui
    coqui: {}
```
# Requirements:
`sudo apt install libsndfile1 espeak espeak-ng`

Necessary for recording audio files