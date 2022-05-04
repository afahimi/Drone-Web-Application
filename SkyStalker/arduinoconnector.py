import serial
import sys
import glob
import time

class ArduinoConnector():
    def __init__(self, serialPort=""):
        self.arduino = None
        self.findPayload(serialPort) # We need to establish a serial connection with the Arduino

        if self.arduino is None:
            print("Couldn't find payload")
            raise Exception('Payload not found')
        
    def findPayload(self, serialPort):
        ports = []
        if serialPort == "": # If no port is forced, get all the ports
            ports = self.getSerialPorts()
        else:
            ports.append(serialPort)
        print("Serial Ports:", ports)
        
        for portName in ports:
            print("Trying port", portName)
            arduino = serial.Serial(port=portName, baudrate=115200, timeout=1.5, write_timeout=1.5)
            time.sleep(2) # Giving time to Arduino to wake up

            try:
                arduino.write(bytes('UAS', 'utf-8')) # Sending 'UAS' and expecting to get 'UAS' back
            except serial.SerialTimeoutException: # If we get an exception, the port is not open
                continue

            data = arduino.readline()
            data = data.decode("utf-8")
            data = data.strip('\n')
            data = data.strip('\r')

            if data == "UAS":
                print("Found Payload on port", portName)
                self.arduino = arduino
                return

    def getSerialPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def sendMoveCommandToGimbal(self, dict):
        # Converting from -1 to 1 and removing low values
        x = round(100*dict['JoystickX'])
        if abs(x) < 50:
            x = 0
        y = round(100*dict['JoystickY'])
        if abs(y) < 50:
            y = 0

        message = 'move_' + str(x) + '_' + str(y)
        print(message)
        self.arduino.write(bytes(message, 'utf-8'))


if __name__ == '__main__':
    try:
        arduino = ArduinoConnector()
        arduino.sendToGimbal({'JoystickX': -0.5, 'JoystickY': 1})
    except Exception as ex:
        print(ex)