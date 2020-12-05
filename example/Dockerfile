FROM python:3.8-slim

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /

RUN apt-get update \
    && apt-get install -y gcc git libpq-dev python3-dev 

RUN python -m pip install -r /requirements.txt

COPY exampleapp/ /opt/app/
COPY entrypoint.sh /opt/app/
WORKDIR /opt/app
