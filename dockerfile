ARG BASE_IMAGE=python:3.10-slim-bullseye
FROM $BASE_IMAGE as base
FROM base as builder-base


# python env
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# pip
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_NO_CACHE_DIR=1

COPY ./data /home/data
COPY ./frontend /home/frontend
COPY ./requirements.txt /home/frontend

WORKDIR /frontend
# add streamlit user
# ARG USER_UID=998
# ARG USER_GID=1

USER root
RUN apt-get update && apt-get install -y \
   # curl \
#   htop \
  git \
  build-essential \
#   default-jdk-headless \
  && rm -rf /var/lib/apt/lists/*

# USER streamlit

WORKDIR /home/frontend

RUN pip3 install -r requirements.txt


EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]