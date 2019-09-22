from gpiozero import RGBLED

class Led:
  
  self.color = {"r" : 0,"g" : 0,"b" : 0}


  def __init__(self, color, pins):
    self.color = color
    pins = (16, 20, 21)
    r_pin, g_pin, b_pin = pins
    self.led = RGBLED(r_pin, g_pin ,b_pin, active_high=False, pwm=True)
    
  def setR(self, red):
    self.color = "r" : red,"g" : self.color["g"], "b" : self.color["g"]}
  
  def updateLED(self):
    self.led.color = self.color
