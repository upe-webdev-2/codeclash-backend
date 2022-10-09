# syntax=docker/dockerfile:1

FROM python:3.8-alpine

RUN mkdir /competitive_programming_backend
WORKDIR /competitive_programming_backend

COPY . /competitive_programming_backend/

RUN pip install -e .

EXPOSE 5000

ENTRYPOINT ["flask", "--app", "competitive_programming_backend", "run", "-h", "0.0.0.0", "-p", "5000"]