FROM python:3.11-slim-bullseye

WORKDIR /pytest-src

COPY ./*.py pyproject.toml poetry.lock README.md ./
COPY openmldb_exporter ./openmldb_exporter

RUN pip install --no-cache-dir poetry && \
    poetry install

ENTRYPOINT ["poetry", "run", "pytest"]
