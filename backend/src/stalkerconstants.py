from enum import Enum

url = 'http://127.0.0.1:6923'
port = 6923

class Mission(Enum):
    NO_MISSION      = 0
    USC_2022_TASK_1 = 1
    USC_2022_TASK_2 = 2

class ControlMode(Enum):
    MANUAL  = 0
    AUTO    = 1