#!/usr/bin/env bash

# Run the application.
if [ "$API_PRODUCTION" = "true" ]; then
  # https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes
  echo "Запуск приложения в продакшн-режиме..."
  eval uv run fastapi run src/main.py --host 0.0.0.0 --port "$PORT"
else
  echo "Запуск приложения в режиме разработки..."
  eval uv run fastapi dev src/main.py --host 0.0.0.0 --port "$PORT" --reload
fi
