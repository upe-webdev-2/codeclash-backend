# syntax=docker/dockerfile:1

FROM python:3.8-alpine

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install -e .

EXPOSE 5000

ENTRYPOINT ["flask", "--app", "codeclash_backend", "run", "-h", "0.0.0.0", "-p", "5000"]