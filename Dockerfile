
FROM python:3.8-slim-buster as base
WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry
RUN poetry install
EXPOSE 5000

FROM base as development
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

FROM base as production
ENV FLASK_ENV=production
COPY . /app/
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:5000 todo_app.wsgi:app

FROM base as test
RUN apt-get update && apt-get install curl -y
RUN apt-get update && apt-get install wget -y
#Install chrome
RUN ls -lrt /etc/apt
RUN apt-get update && apt-get install -y gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install google-chrome-stable -y
ENV PYTHONPATH /app:$PATH
ENTRYPOINT ["poetry", "run", "pytest"]

