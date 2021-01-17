FROM python:3.8-slim AS builder

WORKDIR /mlapi

RUN apt-get update && \
    apt-get install -y wget build-essential cmake && \
    apt-get install -y libgl1 libglib2.0-0 libev-dev && \
    apt-get clean

#COPY get_models.sh /mlapi/get_models.sh
#RUN ./get_models.sh

COPY requirements.txt /mlapi/

RUN pip3 install -r requirements.txt && \
    pip3 install 'opencv-python>4.3' && \
    rm -rf $HOME/.cache

COPY . /mlapi
COPY mlapiconfig-docker.ini /mlapi/mlapiconfig.ini

ENV MLAPI_USER MLAPI_PASSWORD MLAPI_SECRET_KEY

EXPOSE 5000

ENTRYPOINT /bin/bash
