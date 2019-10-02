from audio import Audio, Parser
from queue import Queue
from StateEnum import StateEnum
from visual import Color, Led

init_color = Color(255, 255, 255)
pins = (16, 20, 21)

led = Led(init_color, pins)

# TODO: make this set the Color of the LEDs
def setLED(color: Color):
    led.setColor(color)

# This function is called from within the Parser
def action(actionType:StateEnum, color:Color=Color(0,0,0)):
    # The states are seperated into 2 as 'actions' and `set color`
    actions = [StateEnum.ON, StateEnum.OFF, StateEnum.BLINK]
    # We might want to do additional stuff if the state is an action
    if actionType in actions:
        print("State:", actionType.name)
    elif actionType == StateEnum.NOT_UNDERSTOOD:
        print("Vocab:", list(Parser().vocab.keys()))
    elif actionType == StateEnum.CHANGE_COLOR:
        # Change the color of the LEDs
        setLED(color)

# This function runs on the main thread, which handles the machine state
# Such as the colors of the LEDs and indicator lights.
def main():
    # Create and store the event queue in the main thread
    # The queue keeps the events that happen during listening to the audio
    # These events are:
    # SENDING, LISTENING, ERROR, NOT_UNDERSTOOD and OK
    q = Queue()
    # Pass the reference of the queue to the Audio object so that it can add
    # items to it
    a = Audio(q)
    # The parser checks for meaning in the text and runs corresponding functions
    p = Parser()
    # Start the audio recognition thread
    a.start()
    # Run the main thread
    while a.running:
        try:
            # The execution of the main thread will stop here and wait for  
            # a new item in the queue
            result = q.get()
            # The results are the states listed above 
            if result == StateEnum.SENDING:
                print("Sending...")
            elif result == StateEnum.LISTENING:
                print("Listening...")
            elif result == StateEnum.ERROR:
                print("Error!")
            elif result == StateEnum.NOT_UNDERSTOOD:
                print("Not understood!")
            else:
                # Not explicitly checking for the OK state because if the speech is understood
                # the value of result will be a string
                print("You said:", result)
                p.parse(result, action)
            
            q.task_done()
        except:
            # (KeyboardInterrupt, SystemExit)
            a.stop()
            quit()
    # Stop the threads
    a.stop()

# Run the program
if __name__ == "__main__":
    main()