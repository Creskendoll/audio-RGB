from StateEnum import StateEnum
from visual import Color

class Parser(object):
    def __init__(self):
        """Parser initiate vocabulary.

        The parser vocab is made out of colors and actions.
        More keywords can be added to the dicts.
        """
        # TODO: Add more colors
        self.colors = {
            "red": Color(255,0,0),
            "green": Color(0,255,0),
            "blue": Color(0,0,255),
            "yellow": Color(255,255,0),
            "cyan": Color(0,255,255),
            "pink": Color(255,192,203),
            "magenta": Color(255,0,255),
            "white": Color(255,255,255)
        }
        self.actions = {
            "off": StateEnum.OFF,
            "on": StateEnum.ON,
            "blink": StateEnum.BLINK,
            "flash": StateEnum.BLINK,
            "disco": StateEnum.BLINK
        }
        # Known words
        self.vocab = {**self.colors, **self.actions}

    
    def parse(self, s:str, callback):
        """Parse text and execute a callback.

        A string and a callback function of (StateEnum) -> void must be passed.
        The function will check for words in the text and either return a color or an action.
        """
        s = s.lower().split()
        understood = False

        # Check if a known word is inside the text
        for word in s:
            # If the word is an action
            if word in self.actions.keys():
                # We don't need to pass a color 
                callback(self.vocab[word])
                understood = True
                # Break the loop once we find a vocab word in the sentence
                break
            # If the word is a color
            elif word in self.colors.keys():
                # Pass the color to the callback function
                callback(StateEnum.CHANGE_COLOR, self.vocab[word])
                understood = True
                # Break the loop once we find a vocab word in the sentence
                break

        if not understood and callback:
            callback(StateEnum.NOT_UNDERSTOOD)