# syntax=docker/dockerfile:1

FROM python:3.8-alpine

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install -e .

RUN prisma migrate dev

EXPOSE 8000

RUN ["prisma", "generate"]

ENTRYPOINT ["python", "startup.py"]