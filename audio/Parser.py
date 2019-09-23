from StateEnum import StateEnum
from visual import Color

class Parser(object):
    def __init__(self):
        # TODO: Add more colors
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
        # Known words
        self.vocab = {**self.colors, **self.actions}

    def parse(self, s:str, callback=None):
        s = s.lower()
        # Check if a known word is inside the text
        for word in self.vocab.keys():
            word = word.lower()
            # If the word is a color
            if word in s and word in self.colors.keys():
                if callback:
                    # Pass the color to the callback function
                    callback(StateEnum.CHANGE_COLOR, self.vocab[word])
                break
            # If the word is an action
            elif word in s and word in self.actions.keys():
                if callback:
                    # We don't need to pass a color 
                    callback(self.vocab[word])
                break
            