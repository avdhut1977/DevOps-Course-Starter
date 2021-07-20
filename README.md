# DevOps Apprenticeship: Project Exercise

## Getting started
The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On Windows

Setup the below Environment variables for Trello API

TRELLO_KEY

TRELLO_TOKEN

TRELLO_BOARD

TRELLO_TODO_LIST_ID

TRELLO_DOING_LIST_ID

TRELLO_DONE_LIST_ID


## Running the App on VM

```bash
vagrant up
```
## Running within Docker

### Building docker image
To build the docker image run the following command

```
docker build --target development --tag todo-app:dev .
docker build --target production --tag todo-app:prod .
docker build --target test --tag my-test-image .
```

### Running the container

To run the production container as a daemon run following command
```
docker run --env-file ./.env -p 5000:5000  todo-app:prod
```

To run the development container as a daemon ensure you mount the project directory within the container e.g. run following command
```
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app/ todo-app:dev
```
To run the test container as a daemon ensure you mount the project directory within the container e.g. run following command
```
docker run --env-file ./.env -p 5000:5000  my-test-image
```
## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
Trello Key and Token has been set in .env to use Trello APIs
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

##  App on Heroku
```
https://trello-to-do-app.herokuapp.com/

```

### Database setup
Setup below environment variable for Database connections
```
MONGO_DB_URL ( required)
MONGO_DB_NAME (optional)
ITEMS_TABLE_NAME (optional)

Default values
MONGO_DB_NAME=Board
ITEMS_TABLE_NAME=Items
```
## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
