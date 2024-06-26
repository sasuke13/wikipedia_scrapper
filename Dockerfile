FROM python:3.10

RUN apt update

RUN mkdir "scrapper"

WORKDIR /scrapper

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./poetry.lock ./
COPY ./pyproject.toml ./

RUN python -m pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY ./src ./src
COPY ./commands ./commands

RUN chmod +x commands/*.sh
