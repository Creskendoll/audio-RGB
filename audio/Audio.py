import speech_recognition as sr  
from threading import Thread
from StateEnum import StateEnum

class Audio(object):

    # Takes in a Queue pointer 
    def __init__(self, queue):
        # Speech recognizer
        self.r = sr.Recognizer()
        # Keep thread None when not being used
        self.recognize_thread = None
        # Store the queue pointer
        self.queue = queue

    # Start listening
    def startRecognizing(self):
        if not self.recognize_thread:
            self.recognize_thread = Thread(target=self.recognize, args=())
            self.recognize_thread.start()

    # Stop listening
    def stopRecognizing(self):
        # Stop and reset the thread
        self.recognize_thread.join()
        self.recognize_thread = None

    # Runs async and populates the queue with states and strings
    def recognize(self, *args):
        with sr.Microphone() as source:
            # Run continuously
            while True:
                # Update queue
                self.queue.put(StateEnum.LISTENING)
                self.r.adjust_for_ambient_noise(source)
                # The execution stops until a sentence is heard
                audio = self.r.listen(source)
                self.queue.put(StateEnum.SENDING)
                try:
                    # Send the audio to google and get the response
                    self.queue.put(self.r.recognize_google(audio))
                # Error handling
                except sr.UnknownValueError:
                    self.queue.put(StateEnum.NOT_UNDERSTOOD)
                except sr.RequestError as e:
                    print(e)
                    self.queue.put(StateEnum.ERROR)
