#!/bin/bash
echo "Port: $PORT"
poetry run gunicorn  "todo_app.wsgi:app" --bind 0.0.0.0:${PORT}
