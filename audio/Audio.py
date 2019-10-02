import speech_recognition as sr  
from threading import Thread
from StateEnum import StateEnum
# http://docs.kitt.ai/snowboy/#downloads
# import snowboydecoder

class Audio(object):

    # Takes in a Queue pointer 
    def __init__(self, queue):
        # Speech recognizer
        self.r = sr.Recognizer()
        # Keep thread None when not being used
        self.running = False
        # Store the queue pointer
        self.queue = queue
        # self.hot_word_detector = snowboydecoder.HotwordDetector("../jarvis.pmdl", sensitivity=0.5)

    # Start listening
    def start(self):
        if not self.running:
            self.running = True
            self.recognize_thread = Thread(target=self.recognize, args=())
            self.recognize_thread.start()

    # Stop listening
    def stop(self):
        if self.running:
            # Stop and reset the thread
            self.running = False
            self.recognize_thread.join()

    # Runs async and populates the queue with states and strings
    def recognize(self, *args):
        with sr.Microphone(device_index=None) as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
            # Run continuously
            while self.running:
                try:
                    # Update queue
                    self.queue.put(StateEnum.LISTENING)
                    # The execution stops until a sentence is heard
                    audio = self.r.listen(source)
                    # audio = self.r.record(source, duration=3)
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
                except:
                    #  (KeyboardInterrupt, SystemExit)
                    self.stop()
