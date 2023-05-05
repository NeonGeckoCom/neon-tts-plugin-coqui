FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    espeak-ng

COPY . /tmp/neon-tts-plugin-coqui
RUN pip install wheel && \
    pip install \
    /tmp/neon-tts-plugin-coqui/[docker] --extra-index-url https://download.pytorch.org/whl/cpu

ENTRYPOINT ovos-tts-server --engine coqui --gradio \
--title "🐸💬 - NeonAI Coqui AI TTS Plugin" \
--description "🐸💬 - a deep learning toolkit for Text-to-Speech, battle-tested in research and production" \
--info "more info at [Neon Coqui TTS Plugin](https://github.com/NeonGeckoCom/neon-tts-plugin-coqui), [Coqui TTS](https://github.com/coqui-ai/TTS)" \
--badge "https://visitor-badge-reloaded.herokuapp.com/badge?page_id=neongeckocom.neon-tts-plugin-coqui"