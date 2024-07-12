#! /bin/bash

# データベースを起動するシェルスクリプトです。
# シェルスクリプトと異なるディレクトリからも実行可能です。

readonly SCRIPT_DIRECTORY=$(cd $(dirname $0);pwd)
readonly DOCKER_COMPOSE_FILENAME="docker-compose.yaml"

# 「docker-compose up database」を実行する。
# poetry run python -m $SCRIPT_DIRECTORY/api.migrate_database
docker-compose -f $SCRIPT_DIRECTORY/$DOCKER_COMPOSE_FILENAME exec api poetry run python -m src.migrate_database
