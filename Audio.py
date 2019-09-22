
import speech_recognition as sr  
from threading import Thread

class Audio:

    def __init__(self):
        self.r = sr.Recognizer()
        self.recognize_thread = None

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
                yield "Listening"
                audio = self.r.listen(source)   
                yield "Sending"
                try:
                    yield self.r.recognize_google(audio)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
