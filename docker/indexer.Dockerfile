FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app
COPY poetry.lock poetry.toml pyproject.toml ./
RUN poetry install

COPY common ./common
COPY indexer ./indexer

ENTRYPOINT [ "poetry", "run", "python", "-m", "indexer" ]