import requests
from flask import Flask,request,render_template, redirect,url_for
from todo_app.flask_config import Config
from todo_app.Task import Task

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
    json_response = requests.request("GET", url, params=queryparams).json()
    response_string = [] 
    for json_record in json_response:
        response_string.append({'id': json_record['id'], 'name': json_record['name']}) 
    return response_string


def get_board(id):
    url = f"https://api.trello.com/1/boards/{id}"
    queryparams = {"key": key, "token": token}
    json_response = requests.request("GET", url, params=queryparams).json()
    board = {"id": id, "name": json_response['name'] }    
    return board

def get_statuses(id):
    url = f"https://api.trello.com/1/boards/{id}/lists"
    queryparams = {"key": key, "token": token}
    json_response = requests.request("GET", url, params=queryparams).json()  
    data = [] 
    for json_record in json_response:
        data.append({'id': json_record['id'], 'name': json_record['name']}) 
    return data

def get_task(id):
    url = f"https://api.trello.com/1/cards/{id}"
    queryparams = {"key": key, "token": token}
    json_response = requests.request("GET", url, params=queryparams).json()  
    task = Task(id=json_response['id'], status_id=json_response['idList'], name=json_response['name'], status_name='')
    board_id = json_response['idBoard']
    return task , board_id

def delete_task_id(id):
    url = f"https://api.trello.com/1/cards/{id}"
    queryparams = {"key": key, "token": token}
    response = requests.request("DELETE", url, params=queryparams)
    return response.text

def create_task(status_id, task_name):
    url = f"https://api.trello.com/1/cards"
    queryparams = {"name": task_name, "idList": status_id, "key": key, "token": token}
    json_response = requests.request("POST", url, params=queryparams).json()
    taskId = json_response["id"]
    return taskId

def move_task_status(status_id, taskId):
    url = f"https://api.trello.com/1/cards/{taskId}"
    queryparams= {"id": taskId, "idList": status_id, "key": key, "token": token}
    json_response = requests.request("PUT", url, params=queryparams).json()
    taskId = json_response["id"]
    return taskId

def create_status(board_id, status_name):
    statuses = get_statuses(board_id)
    exists = False
    for status in statuses:
        if (status_name == status['name']):
            exists = True
    if (exists == False):
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        queryparams = {"name": status_name, "key": key, "token": token}
        json_response = requests.request("POST", url, headers=headers, params=queryparams).json()
        status_id = json_response["id"]
        return status_id

def create_board(boardName):
    url = "https://api.trello.com/1/boards/"
    queryparams = {"name": boardName, "key": key, "token": token}
    json_response = requests.request("POST", url, params=queryparams).json()
    board_id = json_response["shortUrl"].split("/")[-1].strip()
    return board_id

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
    board_id = request.args.get('id')  
    delete_board_id(board_id)
    return redirect(url_for('index'))

@app.route('/add_status', methods=['GET', 'POST'])
def add_status():    
    if request.method == 'POST':
        board_id = request.form['board_id']
        status_name = request.form['status_name']
        create_status(board_id, status_name)
        return redirect(url_for('view_board', id=board_id))
    else:
        board_id = request.args.get('board_id')
        board = get_board(board_id)    
        return render_template("add_status.html", board=board)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():    
    if request.method == 'POST':
        task_name = request.form['task_name']
        status_id = request.form['status_id']
        board_id = request.form['board_id']         
        create_task(status_id, task_name)
        return redirect(url_for('view_board', id=board_id))
    else:
        board_id = request.args.get('board_id')
        statuses = get_statuses(board_id)
        return render_template("add_task.html", board_id=board_id, statuses=statuses)

@app.route('/move_task', methods=['GET', 'POST'])
def move_task():
    if request.method == 'POST':
        id = request.form['id']        
        board_id = request.form['board_id'] 
        status_id = request.form['status_id']                       
        move_task_status(status_id, id)
        return redirect(url_for('view_board', id=board_id))
    else:
        board_id = request.args.get('board_id')
        taskId = request.args.get('task_id')
        statuses = get_statuses(board_id)
        task , board_id = get_task(taskId)        
        return render_template("move_task.html", task=task, board_id=board_id , statuses=statuses)


@app.route('/delete_task')
def delete_task():
    taskId = request.args.get('task_id')    
    board_id = request.args.get('board_id')
    delete_task_id(taskId)
    return redirect(url_for('view_board', id=board_id))



@app.route('/delete_status')
def delete_status():
    status_id = request.args.get('status_id')    
    board_id = request.args.get('board_id')
    delete_status_id(status_id)
    return redirect(url_for('view_board', id=board_id))


@app.route('/view_board', methods=['GET', 'POST'])
def view_board():
    board_id = request.args.get('id')    
    board = get_board(board_id)
    statuses = get_statuses(board_id)
    tasks = []
    for status in statuses:
        status_id = status['id']
        status_name = status['name']
        status_tasks = get_tasks(status_id)
        for task in status_tasks:
            tasks.append(Task(id=task['id'], status_id=status_id, name=task['name'], status_name=status_name) ) 
    return render_template("trello.html", board=board, statuses=statuses, tasks=tasks)

@app.route('/', methods=['GET', 'POST'])
def index():

    url = "https://api.trello.com/1/members/me/boards"
    queryparams = {"key": key, "token": token}
    url_response = requests.request("GET", url, params=queryparams)
    response_string = [] 
    json_string = url_response.json()
    for json_record in json_string:
        response_string.append({'id': json_record['id'], 'name': json_record['name']}) 
    return render_template("index.html", data=response_string)

if __name__ == '__main__':
    app.run()

