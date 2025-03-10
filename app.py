import os
import sys
import time
import argparse
from src import main
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock







templateDir = os.path.abspath('src/frontend/templates')
staticDir = os.path.abspath('src/frontend/static')
app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)
sockerIO = SocketIO(app)

thread = None
threadLock = Lock()

def blueBerry():
    #main.main(task=True)
    while 1:
        print("hello")
        time.sleep(5)

@app.route("/", methods=['POST', 'GET'])
def frontendFunction():
    global thread
    with threadLock:
        if thread is None:
            thread = sockerIO.start_background_task(blueBerry)

    if request.method == "POST":
        #implement a script to update mode / font / download song
        print(str(request))
    
    
    return render_template('index.html')


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--terminal", default=None, 
                        help="No UI")
    parser.add_argument("--download", default=None, 
                        help="Download Current Spotify Song")
    args = parser.parse_args()

    



if __name__ == '__main__':
    #socketIO.run(app)
    run()
