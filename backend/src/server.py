# Will be running on the ground control station
import eventlet
import socketio
import flask
from flask_socketio import SocketIO
from flask import request
import controller
import threading
import time
from stalkerconstants import *
from directorycheck import DirectoryCheck
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

socketio = SocketIO(app, async_mode="threading", cors_allowed_origins={'*'})

stalkerStatus = {'mission': Mission.USC_2022_TASK_2.value,
                 'controlMode': ControlMode.MANUAL.value, 'boundingBox': None}

l = DirectoryCheck()

@app.route('/largest', methods=['GET'])
def largest_endpoint():
    l.updateLargest()
    print(l.largest)
    return str(l.largest)

# Continously reads the controller input and emits an event if there is a change
# This function should be changed so that there is a feedback loop. Currently it emits controller_event signal
# even if the controls did not change. To reduce network cost, we should implement a feedback system. Also
# we should use absolute angles (metadata from images) rather than relative angles.
def read_controller():
    while True:
        if stalkerStatus['controlMode'] == ControlMode.MANUAL.value:
            (is_command_new, command) = controller_input.read(stalkerStatus['mission'])
            print("controller_event:", command)
            socketio.emit('controller_event', data=(stalkerStatus, command))
        time.sleep(0.2)

# Controller
controller_input = controller.XboxController()
controller_read_thread = threading.Thread(target=read_controller, args=())
controller_read_thread.daemon = True
controller_read_thread.start()

# Sends update to StalkerStatus
def emit_ss_update():
    socketio.emit('SS update', stalkerStatus)

# Every so often send an SS update to make sure the AirStalker is up-to-date
# just in case it did not recieve a previous SS update.
def continously_send_ss_update():
    while True:
        emit_ss_update()
        time.sleep(3)

ss_update_thread = threading.Thread(target=continously_send_ss_update, args=())
ss_update_thread.daemon = True
ss_update_thread.start()

# Call this function to update the control mode
@app.route('/controlmode', methods=['POST'])
def updateControlMode():
    input_json = request.get_json(force=True)
    print('data from client:', input_json)
    stalkerStatus['controlMode'] = input_json["mode"]
    emit_ss_update()
    return flask.jsonify(input_json)

# Call this function to update the mission
@app.route('/missionstatus', methods=['POST'])
def updateMission():
    input_json = request.get_json(force=True)
    print('data from client:', input_json)
    stalkerStatus['mission'] = input_json["mission"]
    emit_ss_update()
    return flask.jsonify(input_json)

# Call this function to update the bounding box
def updateBoundingBox(boundingBox):
    stalkerStatus['boundingBox'] = boundingBox
    emit_ss_update()

@socketio.event
def connect():
    print('Connected')
    emit_ss_update()

@socketio.event
def test_message(data):
    print('Recieved message: ', data)

@socketio.event
def disconnect():
    print('Disconnected')

if __name__ == '__main__':
    socketio.run(app, port=port)
