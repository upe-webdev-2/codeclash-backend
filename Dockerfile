# syntax=docker/dockerfile:1

FROM python:3.8-alpine

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install -e .
RUN pip install --upgrade pip

EXPOSE 8000

RUN pip install -U git+https://github.com/RobertCraigie/prisma-client-py@refactor/remove-pkg-cli

RUN ["prisma", "generate"]

ENTRYPOINT ["python", "startup.py"]
