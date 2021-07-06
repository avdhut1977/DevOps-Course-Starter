from todo_app.app import create_app
from todo_app.mongo_db_tasks import TasksDb

taskDb = TasksDb()
app = create_app(taskDb)