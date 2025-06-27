FROM python:3.9-slim AS compile-image

COPY . /tmp/neon-tts-plugin-coqui

RUN pip install --no-cache-dir wheel && \
    pip install --user --no-cache-dir \
    /tmp/neon-tts-plugin-coqui/[docker] --extra-index-url https://download.pytorch.org/whl/cpu

# Copy built packages to a clean image to exclude build-time extras from final image
FROM python:3.9-slim AS build-image
COPY --from=compile-image /root/.local /root/.local
COPY docker_overlay /
ENV PATH=/root/.local/bin:$PATH

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    espeak-ng \
    curl \
    jq

HEALTHCHECK CMD "/opt/neon/healthcheck.sh"
ENTRYPOINT ["ovos-tts-server", "--engine", "coqui", "--gradio", \
"--title", "🐸💬 - Neon AI Coqui AI TTS Plugin", \
"--description", "🐸💬 - a deep learning toolkit for Text-to-Speech, battle-tested in research and production", \
"--info", "more info at [Neon Coqui TTS Plugin](https://github.com/NeonGeckoCom/neon-tts-plugin-coqui), [Coqui TTS](https://github.com/coqui-ai/TTS)"]
