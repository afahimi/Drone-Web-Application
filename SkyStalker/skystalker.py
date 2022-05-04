# To be run on the aircraft
import socketio
import sys
import threading
import argparse
from tracker import Tracker
from arduinoconnector import ArduinoConnector
sys.path.append('../backend/src/')
from stalkerconstants import *
sys.path.append('./aeac_controls_2022/')
from uasdriver import UASDriver

stalkerStatus = {'mission': Mission.NO_MISSION.value, 'controlMode': ControlMode.MANUAL.value, 'boundingBox': None}
trackerEnabled = False
sio = socketio.Client()

arduino = None
tracker = None
uasdriver = None

# Called by Tracker to send commands to payload
def tracker_send_command_to_payload(command):
    if stalkerStatus['mission'] != Mission.USC_2022_TASK_2.value or stalkerStatus['controlMode'] != ControlMode.AUTO.value:
        print("ERROR: Tracker attempted to send a command when it shouldn't.", Mission(stalkerStatus['mission']), ControlMode(stalkerStatus['controlMode']))
        return
    send_command_to_payload(command)

# Sends commands to payload based on the mission
def send_command_to_payload(command):
    if stalkerStatus['mission'] == Mission.USC_2022_TASK_1.value:
        if uasdriver is None:
            print("ERROR: Attempted to send commands to UASDriver when it is not initialized")
            return
        print("Sending controls to payload: ", command)
        # Need to invert buttons
        uasdriver.setRemoteValues(int(not command['A']), int(not command['B']), int(not command['X']), int(not command['Y']), \
            command['LeftJoystickX'], command['LeftJoystickY'], int(not command['LeftThumb']), \
            command['RightJoystickX'], command['RightJoystickY'], int(not command['RightThumb']) )
    elif stalkerStatus['mission'] == Mission.USC_2022_TASK_2.value:
        if arduino is None:
            print("ERROR: Attempted to send commands to Arduino when it is not initialized")
            return
        print("Sending controls to payload: ", command)
        arduino.sendMoveCommandToGimbal(command)
    else:
        print("ERROR: A command was tried to be sent to payload but no payload is specified for", Mission(stalkerStatus['mission']))

# Called when connected to the server
@sio.event
def connect():
    print('Connected')

# Called when disconnected from the server
@sio.event
def disconnect():
    print('Disconnected')

# Called when a controller event is caught
@sio.event
def controller_event(ss, data):
    check_SS_change(ss)

    if stalkerStatus['controlMode'] != ControlMode.MANUAL.value:
        return
    send_command_to_payload(data)

# StalkerStatus update checksq
@sio.on('SS update')
def check_SS_change(ss):
    tracker_status_can_change = False
    if stalkerStatus['mission'] != ss['mission']:
        update_mission(ss)
        tracker_status_can_change = True
    if stalkerStatus['controlMode'] != ss['controlMode']:
        update_control_mode(ss)
        tracker_status_can_change = True
    if tracker_status_can_change:
        update_tracker_status() # Enable or disable Tracker
    if stalkerStatus['boundingBox'] != ss['boundingBox']:
        update_bounding_box(ss)

# For handling a change of the mission mode
def update_mission(ss):
    global arduino, tracker, uasdriver
    print("Updating mission mode from", Mission(stalkerStatus['mission']), "to", Mission(ss['mission']))
    stalkerStatus['mission'] = ss['mission']

    if ss['mission'] == Mission.USC_2022_TASK_2.value:
        if arduino is None:
            try:
                arduino = ArduinoConnector()
                print("Arduino initialized")
            except Exception as ex:
                print(ex)
        if tracker is None:
            try:
                tracker = Tracker(tracker_send_command_to_payload)
                print("Tracker initialized")
            except Exception as ex:
                print(ex)
    elif ss['mission'] == Mission.USC_2022_TASK_1.value:
        if uasdriver == None:
            try:
                uasdriver = UASDriver()
                uasdriver_thread = threading.Thread(target=uasdriver.controlLoop, daemon=True)
                uasdriver_thread.start()
                print("UASDriver initialized")
            except Exception as ex:
                print(ex)

# For handling a change of the control mode
def update_control_mode(ss):
    print("Updating control mode from", ControlMode(stalkerStatus['controlMode']), "to",  ControlMode(ss['controlMode']))
    stalkerStatus['controlMode'] = ss['controlMode']

# For handling a change of the bounding box
def update_bounding_box(ss):
    if stalkerStatus['mission'] != Mission.USC_2022_TASK_2.value:
        print("ERROR: Got an update to the bounding box but the mission is not set to USC Task 2. Ignoring update.")
        return
    if tracker is None:
        print("ERROR: Got an update to the bounding but Tracker is not initialized")
    print("Updating bounding box from", stalkerStatus['boundingBox'], "to",  ss['boundingBox'])
    stalkerStatus['boundingBox'] = ss['boundingBox']
    tracker.updateBoundingBox(stalkerStatus['boundingBox'])

# For enabling or disabling tracker
def update_tracker_status():
    if tracker is None:
        return
    if stalkerStatus['mission'] == Mission.USC_2022_TASK_2.value and stalkerStatus['controlMode'] == ControlMode.AUTO.value:
        print("Enabling Tracker")
        tracker.setEnabled(True)
    else:
        print("Disabling Tracker")
        tracker.setEnabled(False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default=url)
    io_args = parser.parse_args()
    ground_stalker_url = io_args.url

    sio.connect(ground_stalker_url)
    sio.wait()
