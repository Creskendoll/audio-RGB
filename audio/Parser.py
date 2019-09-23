from StateEnum import StateEnum

class Parser(object):
    def __init__(self):
        self.vocab = {
            "red", "green", "blue", "off", "on", "flash"}

    def parse(self, s):
        for word in self.vocab:
            if word in s:
                pass
