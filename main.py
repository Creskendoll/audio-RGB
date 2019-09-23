from audio import Audio
from queue import Queue
from audio import Parser
from StateEnum import StateEnum
from visual.Color import Color

def setLED(color):
    print(color)

def action(actionType:StateEnum, color:Color=Color()):
    actions = [StateEnum.ON, StateEnum.OFF, StateEnum.BLINK]
    if actionType in actions:
        print("Action")
    else:
        setLED(color)

def main():
    q = Queue()
    a = Audio(q)
    p = Parser()
    a.startRecognizing()
    while True:
        w = q.get()
        if w is None: continue
        
        if w == StateEnum.SENDING:
            print("Sending...")
        elif w == StateEnum.LISTENING:
            print("Listening...")
        elif w == StateEnum.ERROR:
            print("Error!")
        elif w == StateEnum.NOT_UNDERSTOOD:
            print("Not understood!")
        else:
            p.parse(w, callback=action)
        
        q.task_done()
    a.stopRecognizing()

if __name__ == "__main__":
    main()