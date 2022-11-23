ARG BASE_CONTAINER=ubuntu
ARG UBUNTU_VERSION=20.04

FROM $BASE_CONTAINER:$UBUNTU_VERSION

WORKDIR /mipt-admin

COPY main.py /mipt-admin
COPY mongodb.py /mipt-admin
COPY templates /mipt-admin/templates
COPY static /mipt-admin/static
COPY requirements.txt /mipt-admin
COPY logging.conf /mipt-admin

ENV PYTHON_VERSION=3.9

RUN apt-get update && \
    apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3.9-venv

ENV ADMIN_VENV=venv

RUN python3.9 -m venv $ADMIN_VENV \
    && $ADMIN_VENV/bin/pip install -r requirements.txt

CMD $ADMIN_VENV/bin/uvicorn main:app --host 0.0.0.0 --port 8000

