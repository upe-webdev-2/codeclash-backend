# syntax=docker/dockerfile:1

FROM python:3.8-alpine

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN pip install -e .
RUN pip install --upgrade pip

EXPOSE 8000

FROM node
RUN npm install prisma
RUN npx prisma generate

ENTRYPOINT ["python", "startup.py"]
