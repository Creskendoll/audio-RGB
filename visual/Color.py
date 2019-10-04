class Color(object):
    # Simple object to store color
    # Default value is black
    def __init__(self, red=0, green=0, blue=0):
        # All values are between 0 and 255
        assert red >= 0 and red <= 255 and green >= 0 and green <= 255 and blue >= 0 and blue <= 255, \
        "Color values should be between 0 and 255"
        self.red = red
        self.green = green
        self.blue = blue

    # to string method
    def __str__(self):
        return "Color (R:{}, G:{}, B:{})".format(self.red, self.green, self.blue)

    # Returns the normalized RGB values as a tuple
    def getLEDColor(self):
        return (self.red/255.0, self.green/255.0, self.blue/255.0)
