import os
import sys
import time
from rich import print
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock

#This file is wip use terminal.py for now to continue using the application normally


'''
sys.path.insert(1, 'src')
import main
'''

templateDir = os.path.abspath('frontend/templates')
staticDir = os.path.abspath('frontend/static')
app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)
sio = SocketIO(app)

thread = None
threadLock = Lock()

def blueBerry():
    #main.main(task=True)
    while 1:
        print("hello")
        time.sleep(5)

@app.route("/")
def frontendFunction():
    global thread
    with threadLock:
        if thread is None:
            thread = sio.start_background_task(blueBerry)
    return render_template('index.html')


if __name__ == '__main__':
    sio.run(app)
