FROM python:3.10-slim-buster

ARG MY_VARIABLE

ENV DISCORD_TOKEN=${MY_VARIABLE}

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY .env .env
COPY main.py main.py

CMD python main.py