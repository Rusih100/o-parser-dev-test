FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install poetry
RUN poetry install --no-dev --no-root
