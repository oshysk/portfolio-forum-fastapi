# MEMO: ./docker/python/Dockerfileに配置することは無理でした。COPYが上位ディレクトリに対応していないからです。

FROM python:3.12.4-slim

WORKDIR /app
COPY ./pyproject.toml* ./
# COPY ./pyproject.toml* ./poetry.lock* ./
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install

ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
