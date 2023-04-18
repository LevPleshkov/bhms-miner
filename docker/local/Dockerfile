FROM python:3.9.10-alpine

WORKDIR /usr/src/miner

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update \
    && apk add make automake subversion postgresql-dev gcc g++ python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt


COPY ./src ./src


# entrypoint
COPY ./docker/local/entrypoint .
RUN sed -i 's/\r$//g' /usr/src/miner/entrypoint
RUN chmod +x /usr/src/miner/entrypoint

# start django
COPY ./docker/local/start-django .
RUN sed -i 's/\r$//g' /usr/src/miner/start-django
RUN chmod +x /usr/src/miner/start-django

# start celery worker
COPY ./docker/local/start-celeryworker .
RUN sed -i 's/\r$//g' /usr/src/miner/start-celeryworker
RUN chmod +x /usr/src/miner/start-celeryworker

# start celery beat
COPY ./docker/local/start-celerybeat .
RUN sed -i 's/\r$//g' /usr/src/miner/start-celerybeat
RUN chmod +x /usr/src/miner/start-celerybeat


ENTRYPOINT [ "/usr/src/miner/entrypoint" ]
