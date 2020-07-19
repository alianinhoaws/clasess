import re


class CharField:

    def __init__(self, value):
        self.value = value

    def check(self):
        if not re.fullmatch('[A-Z][\w]*', self.value):
            pass
