FROM 618787091844.dkr.ecr.us-east-1.amazonaws.com/python:3.11-slim AS base

RUN adduser --system --no-create-home user

RUN apt-get update

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
WORKDIR /app
COPY src /app

ARG GUNICORN_WORKERS
ENV GUNICORN_WORKERS=$GUNICORN_WORKERS

FROM base as api
RUN chown -R user /app
USER user
CMD gunicorn -c config.py -w $GUNICORN_WORKERS -b 0.0.0.0:3000 -t 60 app

FROM base as consumer
RUN chown -R user /app
USER user
CMD ["python", "app_consumer.py"]