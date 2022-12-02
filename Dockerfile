# syntax=docker/dockerfile:1

FROM python:3.8-alpine

RUN mkdir /codeclash_backend
WORKDIR /codeclash_backend

COPY . /codeclash_backend/

RUN curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | python
RUN pipenv install --system --deploy --ignore-pipfile
RUN prisma generate

EXPOSE 8000

ENTRYPOINT ["python", "startup.py"]
