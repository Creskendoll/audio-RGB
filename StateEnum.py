from enum import Enum
class StateEnum(Enum):
    LISTENING = 0
    SENDING = 1
    OK = 2
    NOT_UNDERSTOOD = 3
    ERROR = 4