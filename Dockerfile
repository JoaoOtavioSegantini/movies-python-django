FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends \
                    default-jre \
                    git \
                    zsh \
                    curl \
                    wget \
                    fonts-powerline

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app

ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src

CMD [ "tail", "-f", "/dev/null" ]
