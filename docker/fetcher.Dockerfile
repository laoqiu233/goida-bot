FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app
COPY poetry.lock poetry.toml pyproject.toml ./
RUN poetry install

RUN poetry run playwright install chromium
RUN poetry run playwright install-deps

COPY common ./common
COPY fetcher ./fetcher

ENTRYPOINT [ "poetry", "run", "python", "-m", "fetcher" ]