FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl

COPY . /app/

RUN pip3 install -r requirements.txt

EXPOSE 8051