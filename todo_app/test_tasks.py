import pytest
import todo_app.view_model as view_model
import datetime
import todo_app.Task as task

    
@pytest.fixture
def test_tasks():
    '''
        Test there are 2 To DO tasks , 3 Tasks with Status as Doing and 4 Done Tasks Today / 3 Tasks Done before today
    '''
    today = datetime.datetime.utcnow()
    yesterday = today - datetime.timedelta(days=1)
    task_list = [
        task.Task(1, 'To Do', 'Task1', today),
        task.Task(2, 'To Do', 'Task2', today),
        task.Task(3, 'Doing', 'Task3', today),
        task.Task(4, 'Doing', 'Task4', today),
        task.Task(5, 'Doing', 'Task5', today),
        task.Task(6, 'Done', 'Task6', today),
        task.Task(7, 'Done', 'Task7', today),
        task.Task(8, 'Done', 'Task8', today),
        task.Task(9, 'Done', 'Task8', today),
        task.Task(10, 'Done', 'Task10', yesterday),
        task.Task(11, 'Done', 'Task11', yesterday),
        task.Task(12, 'Done', 'Task12', yesterday)
    ]

    test_list = view_model.ViewModel(task_list)

    return test_list

@pytest.fixture
def test_tasks_with_4_done():
    today = datetime.datetime.utcnow()
    yesterday = today - datetime.timedelta(days= 1)
    task_list = [ 
        task.Task(1, 'To Do', 'Task1', today),
        task.Task(2, 'To Do', 'Task2', today),
        task.Task(3, 'Doing', 'Task3', today),
        task.Task(4, 'Doing', 'Task4', today),
        task.Task(5, 'Done', 'Task5', today),
        task.Task(6, 'Done', 'Task6', yesterday),
        task.Task(7, 'Done', 'Task7', yesterday),
        task.Task(8, 'Done', 'Task8', yesterday)
    ]
    
    test_list = view_model.ViewModel(task_list)

    return test_list

@pytest.fixture
def test_tasks_with_5_done():
    today = datetime.datetime.utcnow()
    yesterday = today - datetime.timedelta(days= 1)
    task_list = [   
        task.Task(1, 'Doing', 'Task1', today),
        task.Task(2, 'Doing', 'Task2', today),
        task.Task(3, 'Done', 'Task3', today),
        task.Task(4, 'Done', 'Task4', today),
        task.Task(5, 'Done', 'Task5', today),
        task.Task(6, 'Done', 'Task6', yesterday),
        task.Task(7, 'Done', 'Task7', yesterday)
    ]

    test_list = view_model.ViewModel(task_list)

    return test_list

def test_to_do_items_count(test_tasks):
    todo = test_tasks.tasks_todo
    assert len(todo) == 2

def test_doing_items_count(test_tasks):
    doing = test_tasks.tasks_doing
    assert len(doing) == 3

def test_done_items_count(test_tasks):
    done = test_tasks.tasks_done
    assert len(done) == 7

def test_recent_done_tasks_count(test_tasks):
    today_tasks = test_tasks.tasks_recently_done
    assert len(today_tasks) == 4

def test_older_done_tasks_count(test_tasks):
    older_tasks = test_tasks.older_done_tasks
    assert len(older_tasks) == 3

def test_show_all_tasks_more_than_5(test_tasks):
    show_all = test_tasks.show_all_done_tasks
    assert len(show_all) == 4

def test_show_all_tasks_less_than_5(test_tasks_with_4_done):
    show_all = test_tasks_with_4_done.show_all_done_tasks
    assert len(show_all) == 4

def test_show_all_tasks_equal_to_5(test_tasks_with_5_done):
    show_all = test_tasks_with_5_done.show_all_done_tasks
    assert len(show_all) == 5