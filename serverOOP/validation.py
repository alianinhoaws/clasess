import re
from serverOOP.serverException import ServerValidateError, ServerValuesException

class Validate:

    # @property
    # def value(self):
    #     return str(self.value)  # decorate before give to external

    def __init__(self, value):
        if value and isinstance(value, str):
            self.value = value
            #self.value(value)
            self.validate()
        else:
            raise ServerValuesException(value)

    def validate(self):
        pass

    def check_pattern(self, expression, pattern):
        if not re.fullmatch(expression, self.value):
            raise ServerValidateError(self.value, pattern)
        return


class CharField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[A-Z][\w]*'
        pattern = 'Azazazaz'
        return self.check_pattern(expression, pattern)


class TeleField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[0-9]{10}'
        pattern = '+380671230213'
        return self.check_pattern(expression, pattern)


class NameField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[A-Z][\w]*'
        pattern = 'Name'
        return self.check_pattern(expression, pattern)


class DateTimeField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '\d{2}/\d{2}/\d{4}'
        pattern = '22/08/2010'
        return self.check_pattern(expression, pattern)


class NumberField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[\d]*'
        pattern = '1234567'
        return self.check_pattern(expression, pattern)


class CheckArgs(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '=(\w+)'
        print(self.value)
        pattern = '[arg 1]*'
        # return self.check_pattern()
        #if not self.check_pattern(expression, pattern):
        return self.value
