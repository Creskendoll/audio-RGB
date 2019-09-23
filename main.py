from audio import Audio
from queue import Queue
from audio import Parser
from StateEnum import StateEnum
from Color import Color

def lightColor(color):
    pass

def main():
    q = Queue()
    a = Audio(q)
    a.startRecognizing()
    while True:
        w = q.get()
        if w is None: continue
        
        if w == StateEnum.SENDING:
            print("Sending...")
        elif w == StateEnum.LISTENING:
            print("Listening...")
        else:
            print(w)
        
        q.task_done()
    a.stopRecognizing()

if __name__ == "__main__":
    main()