#!/bin/bash
# $APP_PORT comes from docker-compose backend environment
# $VIRTUAL_ENV is uploaded by dockerfile into docker envs
set -e
source $VIRTUAL_ENV/bin/activate
cd /backend/api

gunicorn api.app:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8765 \
  --log-level warning \
  --access-logfile /dev/null \
  --config /deployment/entrypoints/gunicorn_conf.py


# gunicorn app:app \
#--logger-class "logging.gunicorn_patch.CustomLogger" \
# --workers 1 \
# --worker-class uvicorn.workers.UvicornWorker \
# --bind 0.0.0.0:"$APP_PORT" --log-level 'debug'
