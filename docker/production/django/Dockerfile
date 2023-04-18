# # # # # # # # # # # # # # # # # # # #
# # # # # # # # BUILDER # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

FROM python:3.9.10-alpine AS builder

WORKDIR /usr/src/miner

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update \
    && apk add make automake subversion postgresql-dev gcc g++ python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY ./src ./src
RUN flake8 --ignore=E501,F401,W504 src


COPY ./src/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/miner/wheels -r requirements.txt



# # # # # # # # # # # # # # # # # # # #
# # # # # # # #  FINAL  # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

FROM python:3.9.10-alpine

RUN mkdir -p /home/app

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/miner
RUN mkdir $APP_HOME

WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/miner/wheels /wheels
COPY --from=builder /usr/src/miner/requirements.txt .
RUN pip install --no-cache /wheels/*


# entrypoint
COPY ./docker/production/django/entrypoint .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint
RUN chmod +x $APP_HOME/entrypoint

# start django
COPY ./docker/production/django/start-django .
RUN sed -i 's/\r$//g' $APP_HOME/start-django
RUN chmod +x $APP_HOME/start-django

# start celery worker
COPY ./docker/production/django/start-celeryworker .
RUN sed -i 's/\r$//g' $APP_HOME/start-celeryworker
RUN chmod +x $APP_HOME/start-celeryworker

# start celery beat
COPY ./docker/production/django/start-celerybeat .
RUN sed -i 's/\r$//g' $APP_HOME/start-celerybeat
RUN chmod +x $APP_HOME/start-celerybeat


COPY ./src $APP_HOME/src


RUN chown -R app:app $APP_HOME
USER app


ENTRYPOINT [ "/home/app/miner/entrypoint" ]
