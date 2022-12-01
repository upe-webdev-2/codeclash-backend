#!/bin/bash

# reset backend git branch
cd ~/codeclash/codeclash-backend
git fetch && git reset origin/main --hard

# reset frontend git branch
cd ~/codeclash/codeclash-frontend
git fetch && git reset origin/master --hard

# spin down containers
cd ~/codeclash
docker compose -f docker-compose.prod.yml down
# spin containers back up
docker compose -f docker-compose.prod.yml up -d --build
