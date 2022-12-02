# syntax=docker/dockerfile:1

FROM ubuntu

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y 

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip3 install --upgrade pip
RUN pip3 install -e .
RUN pip3 install nodejs-bin

EXPOSE 8000

RUN apt install git -y

RUN pip3 install -U git+https://github.com/RobertCraigie/prisma-client-py@refactor/remove-pkg-cli

RUN ["prisma", "migrate", "deploy"]

RUN ["prisma", "generate"]

ENTRYPOINT ["python3", "startup.py"]
