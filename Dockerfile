# syntax=docker/dockerfile:1

FROM ubuntu

RUN sudo apt update
RUN sudo apt install nodejs
RUN sudo install npm
RUN sudo apt install python3
RUN sudo apt install python3-pip 

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip3 install --upgrade pip
RUN pip3 install -e .

EXPOSE 8000

RUN apt install git

RUN pip3 install -U git+https://github.com/RobertCraigie/prisma-client-py@refactor/remove-pkg-cli

RUN ["prisma", "generate"]

ENTRYPOINT ["python3", "startup.py"]
