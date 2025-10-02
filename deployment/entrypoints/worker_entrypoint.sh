#!/bin/bash
# $APP_PORT comes from docker-compose backend environment
# $VIRTUAL_ENV is uploaded by dockerfile into docker envs
set -e
source $VIRTUAL_ENV/bin/activate
cd /backend/worker

gunicorn worker.app:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level debug \
  --config /deployment/entrypoints/gunicorn_conf.py