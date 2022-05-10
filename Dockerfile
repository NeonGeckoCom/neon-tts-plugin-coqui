FROM python:3.9-buster

RUN apt-get update -y && apt-get install -y libsndfile1 espeak-ng python3-pip
RUN pip3 install TTS==0.6.2

COPY . /tmp/neon-tts-plugin-coqui

RUN pip3 install ovos-tts-server==0.0.2
RUN pip3 install /tmp/neon-tts-plugin-coqui

ENTRYPOINT ovos-tts-server --engine neon-tts-plugin-coqui