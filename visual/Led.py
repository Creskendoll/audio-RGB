from gpiozero import RGBLED
from visual import Color
class Led(object):
    # Takes in an initial color and the pin numbers of the RGB LED
    def __init__(self, color, pins):
        # Unpack the pin values
        r_pin, g_pin, b_pin = pins
        # Init the RGB LED object, we will be using pwm and the color pins of
        # out LED are set to LOW
        self.led = RGBLED(r_pin, g_pin, b_pin, active_high=True, pwm=True)
        self.setColor(color)

    # Set the color of the LED
    def setColor(self, color:Color):
        print("Setting color to:", color.getLEDColor())
        self.led.color = color.getLEDColor()

    def blink(self):
        print("Led is turning on and off.")
        self.led.blink()
        pass
    
    def fade(self, colors):
        # TODO: Fade through the list of colors
        pass 

    def toggleOn(self):
        # Turn on/off the led
        pass

############ Example usage of the class ############
# Green
# init_color = Color(0, 255, 0)
# pins = (16, 20, 21)

# # Init the class
# my_led = Led(init_color, pins)

# # Red
# red_color = Color(255, 0, 0)
# my_led.setColor(red_color)