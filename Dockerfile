FROM python:3.9-slim-bullseye

RUN apt-get update -y && apt-get install -y python3-pip
RUN apt-get update -y && apt-get install -y --no-install-recommends libsndfile1 espeak-ng 

RUN pip3 install torch torchaudio --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip3 install neon-tts-plugin-coqui --no-cache-dir
RUN pip3 install ovos-tts-server==0.0.2 --no-cache-dir

ENTRYPOINT ovos-tts-server --engine neon-tts-plugin-coqui