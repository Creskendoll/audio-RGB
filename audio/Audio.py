
import speech_recognition as sr  
from threading import Thread
from StateEnum import StateEnum

class Audio(object):

    def __init__(self, queue):
        self.r = sr.Recognizer()
        self.recognize_thread = None
        self.queue = queue

    def startRecognizing(self):
        if not self.recognize_thread:
            self.recognize_thread = Thread(target=self.recognize, args=())
            self.recognize_thread.start()

    def stopRecognizing(self):
        self.recognize_thread.join()
        self.recognize_thread = None

    def recognize(self, *args):
        with sr.Microphone() as source:
            while True:
                self.queue.put(StateEnum.LISTENING)
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)
                self.queue.put(StateEnum.SENDING)
                try:
                    self.queue.put(self.r.recognize_google(audio))
                except sr.UnknownValueError:
                    self.queue.put(StateEnum.NOT_UNDERSTOOD)
                except sr.RequestError as e:
                    print(e)
                    self.queue.put(StateEnum.ERROR)
