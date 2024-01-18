FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

CMD gunicorn main:app \
 --log-config ${SRVC_LOG:-/app/settings/logging.conf} \
 --workers 4 \
 --worker-class uvicorn.workers.UvicornWorker \
 --bind 0.0.0.0:8010


