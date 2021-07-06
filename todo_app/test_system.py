import os
import pytest
import todo_app.app as app
from todo_app.trello import create_board, delete_board
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import dotenv
import requests
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager #newly added to resolve hard coding
from todo_app.mongo_db_tasks import TasksDb



@pytest.fixture(scope='module')
def test_app():

    file_path = dotenv.find_dotenv('.env') 
    dotenv.load_dotenv(file_path, override=True)      
    
    db = TasksDb()

    

    # construct the new application   
    application = app.create_app(db)   

    # start the app in its own thread.  
    thread = Thread(target=lambda: application.run(use_reloader=False))  
    thread.daemon = True  
    thread.start()   
    yield app   

    # Tear Down     
    thread.join(1)  
    test_task = db.get_task("TestItem")
    if test_task is not None:
        id = test_task["_id"]        
        db.delete_task(id)



@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(ChromeDriverManager().install(), options=opts) as driver: #newly added
        yield driver       


def test_adding_new_task(driver, test_app):    
    driver.get('http://localhost:5000/')  
    input_field = driver.find_element_by_id('title')
    input_field.send_keys("TestItem")
    add_task = driver.find_element_by_id('new_task')
    add_task.click()    
    page_source = driver.page_source    
    assert "TestItem" in page_source   
