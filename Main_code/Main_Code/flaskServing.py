from flask import Flask, render_template, Response
import time
import json
import cv2
import numpy as np

# flask initiating
app = Flask(__name__)

# Global variable to store the latest frame
latest_frame = None
frame_lock = False

def update_frame(frame):
    global latest_frame, frame_lock
    if frame is not None and not frame_lock:
        frame_lock = True
        latest_frame = frame
        frame_lock = False

# flash camera feed function
def camFeed():
    while True:
        time.sleep(0.1)
        try:
            if app.config.get('frame') and len(app.config['frame']) > 1:
                img = app.config['frame'][1]
                if img:
                    yield (b'--frame\r\n' 
                            b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        except Exception as e:
            print(f"Error in camFeed: {e}")
            time.sleep(0.1)
            continue

#--------------Static serving--------------#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/style.css')
def style():
	return render_template('style.css')

@app.route('/app.js')
def js():
	return render_template('app.js')

@app.route('/video_feed')
def video_feed():
    return Response(camFeed(), mimetype='multipart/x-mixed-replace; boundary=frame')


# routes for the programme functions
@app.route('/start')
def start():
    print('Process started')
    if app.config.get('frame') and len(app.config['frame']) > 2:
        app.config['frame'][2] = True
    return "Process started successfully"

@app.route('/pause')
def pause():
    print('Process paused')
    if app.config.get('frame') and len(app.config['frame']) > 2:
        app.config['frame'][2] = False
    return "Process paused successfully"

@app.route('/home')
def home():
    print('Home command received')
    data = [
        {
            "id": 1,
            "x": 100,
            "y": 100
        },
        {
            "id": 2,
            "x": 200,
            "y": 100
        }
    ]
    if app.config.get('frame') and len(app.config['frame']) > 3:
        app.config['frame'][3] = json.dumps(data)
    return "Home position set successfully"

@app.route('/home_1')
def homeBot_1():
    print('Home Bot 1 command received')
    data = [
        {
            "id": 1,
            "x": 100,
            "y": 100
        }
    ]
    if app.config.get('frame') and len(app.config['frame']) > 3:
        app.config['frame'][3] = json.dumps(data)
    return "Home position set successfully for Bot 1"

@app.route('/home_2')
def homeBot_2():
    print('Home Bot 2 command received')
    data = [
        {
            "id": 2,
            "x": 200,
            "y": 100
        }
    ]
    if app.config.get('frame') and len(app.config['frame']) > 3:
        app.config['frame'][3] = json.dumps(data)
    return "Home position set successfully for Bot 2"

# flask thread
def flaskThread(sharedData):
    app.config['frame'] = sharedData
    app.run("0.0.0.0",3001,debug=False)