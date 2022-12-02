#!/bin/bash

prisma migrate deploy

prisma generate

python3 startup.py
