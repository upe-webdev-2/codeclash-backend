# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install -e .

EXPOSE 8000

RUN ["prisma", "generate"]

ENTRYPOINT ["python", "startup.py"]
