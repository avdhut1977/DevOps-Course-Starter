
FROM python:3.8-slim-buster as base
WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry
COPY poetry.lock .
RUN poetry install
EXPOSE 5000

FROM base as development
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

FROM base as production
ENV FLASK_ENV=production
ENV PORT=5000
COPY run.sh /app
COPY ./todo_app /app/todo_app
RUN chmod +x run.sh
ENTRYPOINT ./run.sh


FROM base as test
#Install chrome
RUN ls -lrt /etc/apt
RUN apt-get update && apt-get install curl wget gnupg2 -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install google-chrome-stable -y
ENV PYTHONPATH /app:$PATH
COPY ./todo_app /app/todo_app
ENTRYPOINT ["poetry", "run", "pytest"]

