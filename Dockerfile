# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install --upgrade pip

RUN pip install -e .

EXPOSE 8000

RUN pip install -U git+https://github.com/RobertCraigie/prisma-client-py@refactor/remove-pkg-cli

ENTRYPOINT ["python", "startup.py"]