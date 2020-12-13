FROM python:3.6-slim

WORKDIR /jp-migrator
ENV PYTHONPATH /jp-migrator

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    libpq-dev \
    python-pip \
    python-setuptools \
    tdsodbc \
    unixodbc \
    unixodbc-dev
    

RUN echo '[ODBC]' >> /etc/odbcinst.ini && \
    echo 'Trace = no' >> /etc/odbcinst.ini && \
    echo '[FreeTDS]' >> /etc/odbcinst.ini && \
    echo 'Description = FreeTDS driver' >> /etc/odbcinst.ini && \
    echo 'Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so' >> /etc/odbcinst.ini && \
    echo 'UsageCount = 1' >> /etc/odbcinst.ini

COPY ./requirements.txt /jp-migrator/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /jp-migrator
