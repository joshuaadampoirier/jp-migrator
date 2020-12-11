FROM ubuntu:16.04

WORKDIR /jp-migrator

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /jp-migrator/requirements.txt

RUN pip install --upgrade pip
    pip install -r requirements.txt

COPY setup.py /jp-migrator/setup.py
COPY .git /allocation/.git

COPY . /jp-migrator