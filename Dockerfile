FROM python:3.9-slim-bullseye AS compile-image

RUN apt-get update -y && apt-get install -y python3-pip git

RUN pip3 install --user torch --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu

COPY . /tmp/neon-tts-plugin-coqui

RUN pip3 install --user /tmp/neon-tts-plugin-coqui --no-cache-dir
# TODO: Figure out why pypi install isn't working
RUN #pip3 install --user ovos-tts-server~=0.0.2 --no-cache-dir
RUN pip3 install --user git+https://github.com/OpenVoiceOS/ovos-tts-server
#FROM python:3.9-slim-bullseye AS build-image

RUN apt-get update -y && apt-get install -y --no-install-recommends espeak-ng 
#COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT ovos-tts-server --engine coqui