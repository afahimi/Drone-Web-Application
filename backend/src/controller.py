from inputs import get_gamepad
from inputs import UnpluggedError
import threading
import time
from stalkerconstants import *

'''
Controller control code.
The returned controls can be changed based on the mission

There are 3 different types of inputs:
Button: Represented by a boolean value
Analog stick: Represented by X and Y flaoting points. Can use arctan to convert to circular coordiantes.
Trigger Button: Represented by a floating point.

The floating point values are normalized between -1 and 1 or 0 and 1. See monitor_controller.

This code is based on
https://stackoverflow.com/questions/46506850/how-can-i-get-input-from-an-xbox-one-controller-in-python
'''

class XboxController(object):
    MAX_TRIG_VAL = 256 # 2^8
    MAX_JOY_VAL = 32768 # 2^15

    last_command = {}

    connected = False

    def __init__(self):
        self.initalize_values()
        self._monitor_thread = threading.Thread(target=self.monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def initalize_values(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

    # Returns the buttons/triggers that are required for the specificed control type (mission)
    # Returns a tuple. First item, whether there is a new command. Second item, command.
    def read(self, mission):
        command = {}
        if mission == Mission.USC_2022_TASK_1.value:
            command = {"A": self.A, "B": self.B, "X": self.X, "Y": self.Y, \
                "LeftJoystickX": self.LeftJoystickX, "LeftJoystickY": self.LeftJoystickY, "LeftThumb": self.LeftThumb, \
                "RightJoystickX": self.RightJoystickX, "RightJoystickY": self.RightJoystickY, "RightThumb": self.RightThumb }
        elif mission == Mission.USC_2022_TASK_2.value:
            command = {"JoystickX": self.LeftJoystickX, "JoystickY": self.LeftJoystickY}
        
        if command == self.last_command:
            return (False, command)
        else:
            self.last_command = command
            return(True, command)

    # Mapping events to varaibles (with conversion when necessary)
    def monitor_controller(self):
        while True:
            try:
                events = get_gamepad()
                self.connected = True
                for event in events:
                    if event.code == 'ABS_Y':
                        self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_X':
                        self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_RY':
                        self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_RX':
                        self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_Z':
                        self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                    elif event.code == 'ABS_RZ':
                        self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                    elif event.code == 'BTN_TL':
                        self.LeftBumper = event.state
                    elif event.code == 'BTN_TR':
                        self.RightBumper = event.state
                    elif event.code == 'BTN_SOUTH':
                        self.A = event.state
                    elif event.code == 'BTN_NORTH':
                        self.X = event.state
                    elif event.code == 'BTN_WEST':
                        self.Y = event.state
                    elif event.code == 'BTN_EAST':
                        self.B = event.state
                    elif event.code == 'BTN_THUMBL':
                        self.LeftThumb = event.state
                    elif event.code == 'BTN_THUMBR':
                        self.RightThumb = event.state
                    elif event.code == 'BTN_SELECT':
                        self.Back = event.state
                    elif event.code == 'BTN_START':
                        self.Start = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY1':
                        self.LeftDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY2':
                        self.RightDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY3':
                        self.UpDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY4':
                        self.DownDPad = event.state
            except UnpluggedError:
                # In the case when a controller is not detected or disconnected, reset all values.
                if self.connected:
                    print("No controller detected")
                    self.initalize_values()
                self.connected = False
            time.sleep(0.05)