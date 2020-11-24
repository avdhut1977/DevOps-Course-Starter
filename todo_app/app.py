import os.path
import os
import requests
from flask import Flask,escape,request,Response,render_template, redirect,url_for
import todo_app.data.session_items as session
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

key = Config.TRELLO_KEY
token = Config.TRELLO_TOKEN

headers = {
   "Accept": "application/json"
}

def get_tasks(s_id):
    url = f"https://api.trello.com/1/lists/{s_id}/cards"
    queryparams = {"key": key, "token": token}
    jsonResponse = requests.request("GET", url, params=queryparams).json()
    responseString = [] 
    for jsonRecord in jsonResponse:
        responseString.append({'id': jsonRecord['id'], 'name': jsonRecord['name']}) 
    return responseString


def get_board(id):
    url = f"https://api.trello.com/1/boards/{id}"
    queryparams = {"key": key, "token": token}
    jsonResponse = requests.request("GET", url, params=queryparams).json()
    board = {"id": id, "name": jsonResponse['name'] }    
    return board

def get_statuses(id):
    url = f"https://api.trello.com/1/boards/{id}/lists"
    queryparams = {"key": key, "token": token}
    jsonResponse = requests.request("GET", url, params=queryparams).json()  
    data = [] 
    for jsonRecord in jsonResponse:
        data.append({'id': jsonRecord['id'], 'name': jsonRecord['name']}) 
    return data

def get_task(id):
    url = f"https://api.trello.com/1/cards/{id}"
    queryparams = {"key": key, "token": token}
    jsonResponse = requests.request("GET", url, params=queryparams).json()  
    task = {'id': jsonResponse['id'], 'name': jsonResponse['name'], 'status_id': jsonResponse['idList'], 'board_id':jsonResponse['idBoard'] }
    return task

def delete_task_id(id):
    url = f"https://api.trello.com/1/cards/{id}"
    queryparams = {"key": key, "token": token}
    response = requests.request("DELETE", url, params=queryparams)
    return response.text

def create_task(statusId, taskName):
    url = f"https://api.trello.com/1/cards"
    queryparams = {"name": taskName, "idList": statusId, "key": key, "token": token}
    jsonResponse = requests.request("POST", url, params=queryparams).json()
    taskId = jsonResponse["id"]
    return taskId

def move_task_status(statusId, taskId):
    url = f"https://api.trello.com/1/cards/{taskId}"
    queryparams= {"id": taskId, "idList": statusId, "key": key, "token": token}
    jsonResponse = requests.request("PUT", url, params=queryparams).json()
    taskId = jsonResponse["id"]
    return taskId

def create_status(boardId, statusName):
    statuses = get_statuses(boardId)
    exists = False
    for status in statuses:
        if (statusName == status['name']):
            exists = True
    if (exists == False):
        url = f"https://api.trello.com/1/boards/{boardId}/lists"
        queryparams = {"name": statusName, "key": key, "token": token}
        jsonResponse = requests.request("POST", url, headers=headers, params=queryparams).json()
        statusId = jsonResponse["id"]
        return statusId

def create_board(boardName):
    url = "https://api.trello.com/1/boards/"
    queryparams = {"name": boardName, "key": key, "token": token}
    jsonResponse = requests.request("POST", url, params=queryparams).json()
    boardId = jsonResponse["shortUrl"].split("/")[-1].strip()
    return boardId

def delete_board_id(id):
    url = f"https://api.trello.com/1/boards/{id}"
    queryparams = {"key": key, "token": token}
    response = requests.request("DELETE", url, params=queryparams)    
    return response.text


def delete_status_id(id):
    url = f"https://api.trello.com/1/lists/{id}/closed"
    queryparams = {"key": key, "token": token}
    response = requests.request("PUT", url, params=queryparams)
    return response.text


@app.route('/add_board', methods=['GET', 'POST'])
def add_board():    
    if request.method == 'POST':
        boardName = request.form['board_name']                
        create_board(boardName)
        return redirect(url_for('index'))
    else:        
        return render_template("add_board.html")

@app.route('/delete_board')
def delete_board():
    boardId = request.args.get('id')  
    delete_board_id(boardId)
    return redirect(url_for('index'))

@app.route('/add_status', methods=['GET', 'POST'])
def add_status():    
    if request.method == 'POST':
        boardId = request.form['board_id']
        statusName = request.form['status_name']
        create_status(boardId, statusName)
        return redirect(url_for('view_board', id=boardId))
    else:
        boardId = request.args.get('board_id')
        board = get_board(boardId)    
        return render_template("add_status.html", board=board)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():    
    if request.method == 'POST':
        taskName = request.form['task_name']
        statusId = request.form['status_id']
        boardId = request.form['board_id']         
        create_task(statusId, taskName)
        return redirect(url_for('view_board', id=boardId))
    else:
        boardId = request.args.get('board_id')
        statuses = get_statuses(boardId)
        return render_template("add_task.html", board_id=boardId, statuses=statuses)

@app.route('/move_task', methods=['GET', 'POST'])
def move_task():
    if request.method == 'POST':
        id = request.form['id']        
        boardId = request.form['board_id'] 
        statusId = request.form['status_id']                       
        move_task_status(statusId, id)
        return redirect(url_for('view_board', id=boardId))
    else:
        boardId = request.args.get('board_id')
        taskId = request.args.get('task_id')
        statuses = get_statuses(boardId)
        task = get_task(taskId)        
        return render_template("move_task.html", task=task, statuses=statuses)


@app.route('/delete_task')
def delete_task():
    taskId = request.args.get('task_id')    
    boardId = request.args.get('board_id')
    delete_task_id(taskId)
    return redirect(url_for('view_board', id=boardId))



@app.route('/delete_status')
def delete_status():
    statusId = request.args.get('status_id')    
    boardId = request.args.get('board_id')
    delete_status_id(statusId)
    return redirect(url_for('view_board', id=boardId))


@app.route('/view_board', methods=['GET', 'POST'])
def view_board():
    boardId = request.args.get('id')    
    board = get_board(boardId)
    statuses = get_statuses(boardId)
    tasks = []
    for status in statuses:
        statusId = status['id']
        statusName = status['name']
        statusTasks = get_tasks(statusId)
        for task in statusTasks:
            tasks.append({'id': task['id'], 'name': task['name'], 's_id': statusId, 's_name': statusName})    
    return render_template("trello.html", board=board, statuses=statuses, tasks=tasks)

@app.route('/', methods=['GET', 'POST'])
def index():

    url = "https://api.trello.com/1/members/me/boards"
    queryparams = {"key": key, "token": token}
    urlResponse = requests.request("GET", url, params=queryparams)
    responseString = [] 
    jsonString = urlResponse.json()
    for jsonRecord in jsonString:
        responseString.append({'id': jsonRecord['id'], 'name': jsonRecord['name']}) 
    return render_template("index.html", data=responseString)

if __name__ == '__main__':
    app.run()

