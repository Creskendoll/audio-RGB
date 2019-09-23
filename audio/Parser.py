from StateEnum import StateEnum
from visual import Color

class Parser(object):
    def __init__(self):
        self.colors = {
            "red": Color(255,0,0),
            "green": Color(0,255,0),
            "blue": Color(0,0,255)
        }
        self.actions = {
            "off": StateEnum.OFF,
            "on": StateEnum.ON,
            "blink": StateEnum.BLINK,
            "flash": StateEnum.BLINK
        }
        self.vocab = {**self.colors, **self.actions}

    def parse(self, s, callback=None):
        for word in self.vocab.keys():
            if word in s and word in self.colors.keys():
                if callback:
                    callback(StateEnum.CHANGE_COLOR, self.vocab[word])
                break
            elif word in self.actions:
                if callback:
                    callback(self.vocab[word])
                break
            