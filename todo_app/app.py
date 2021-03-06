import os
import requests
from flask import Flask, render_template, request, session, redirect, url_for
import todo_app.view_model as view_model
from todo_app.Task import Task
from todo_app.mongo_db_tasks import TasksDb

app = Flask(__name__)
headers = {
   "Accept": "application/json"
}

taskDb = TasksDb()

def create_app(taskDb):
    app = Flask(__name__)    
    
    @app.route('/', methods=['Get'])
    def index():
        tasks = taskDb.get_all_tasks()        
        task_view_model = view_model.ViewModel(tasks)
        return render_template('index.html', view_model=task_view_model)

    @app.route('/add_todo', methods=['Post'])
    def add_todo_task():
        taskDb.create_todo_task(request.form.get('title'))
        return redirect('/')

    @app.route('/move_to_doing/<todo_task_id>', methods=['Post'])
    def move_to_doing(todo_task_id):
        taskDb.move_to_doing(todo_task_id)
        return redirect('/')

    @app.route('/move_to_done/<task_id>', methods=['Post'])
    def move_to_done(task_id):
        taskDb.move_to_done(task_id)
        return redirect('/')

    @app.route('/delete_task/<task_id>', methods=['Post'])
    def remove_task(task_id):
        taskDb.delete_task(task_id)
        return redirect('/') 

    return app



if __name__ == '__main__':
    app = create_app(taskDb)
    app.run()   

   




