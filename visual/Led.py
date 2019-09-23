from gpiozero import RGBLED

class Led(object):
    def __init__(self, color, pins):
        self.color = color
        r_pin, g_pin, b_pin = pins
        self.led = RGBLED(r_pin, g_pin, b_pin, active_high=False, pwm=True)

    def setR(self, red):
        self.color.red = red

    def updateLED(self):
        self.led.color = self.color
