#!/bin/bash

# reset git branch
git fetch && git reset origin/main -- hard
# spin down containers
docker compose -f docker-compose.prod.yml down
# spin containers back up
docker compose -f docker-compose.prod.yml up -d --build
