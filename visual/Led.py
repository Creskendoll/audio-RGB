from gpiozero import RGBLED
from visual import Color

class Led(object):
    # Takes in an initial color and the pin numbers of the RGB LED
    def __init__(self, color, pins):
        self.color = color
        # Unpack the pin values
        r_pin, g_pin, b_pin = pins
        # Init the RGB LED object, we will be using pwm and the color pins of
        # out LED are set to LOW
        self.led = RGBLED(r_pin, g_pin, b_pin, active_high=False, pwm=True)

    # Set the color of the LED
    def setColor(self, color):
        pass

    def setR(self, red):
        self.color.red = red

    def updateLED(self):
        self.led.color = self.color


############ Example usage of the class ############
# Green
init_color = Color(0, 255, 0)
pins = (16, 20, 21)

# Init the class
my_led = Led(init_color, pins)

# Red
red_color = Color(255, 0, 0)
my_led.setColor(red_color)