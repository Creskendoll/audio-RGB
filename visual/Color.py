class Color(object):
    # Simple object to store color
    # Default value is black
    def __init__(self, red=0, green=0, blue=0):
        # All values are between 0 and 255
        self.red = red
        self.green = green
        self.blue = blue

    # to string method
    def __str__(self):
        return "Color (R:{}, G:{}, B:{})".format(self.red, self.green, self.blue)