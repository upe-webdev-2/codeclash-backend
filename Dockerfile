# syntax=docker/dockerfile:1

FROM node:9-slim
RUN apt-get update || : ** apt-get install python -y

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install --upgrade pip

RUN pip install -e .

EXPOSE 8000

RUN apt install git

RUN pip install -U git+https://github.com/RobertCraigie/prisma-client-py@refactor/remove-pkg-cli

RUN ["prisma", "generate"]

ENTRYPOINT ["python", "startup.py"]
