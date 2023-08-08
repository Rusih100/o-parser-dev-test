FROM python:3.11 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

FROM base as dependencies

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-dev --no-root

FROM dependencies as final

COPY . .
