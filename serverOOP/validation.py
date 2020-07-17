import re
from serverOOP.serverException import ServerValidateError, ServerValuesException

class Validate:

    def __init__(self, value):
        if value and isinstance(value, str):
            self.value = value
            self.validate()
        else:
            raise ServerValuesException(value)

    def validate(self):
        pass

    def check_pattern(self, expression):
        if not re.fullmatch(expression, self.value):
            raise ServerValidateError(self.value, expression)
        return


class CharField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[A-Z][\w]*'
        return self.check_pattern(expression)


class TeleField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[0-9]{10}'
        return self.check_pattern(expression)


class NameField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[A-Z][\w]*'
        return self.check_pattern(expression)


class DateTimeField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '\d{2}/\d{2}/\d{4}'
        return self.check_pattern(expression)


class NumberField(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[\d]*'
        return self.check_pattern(expression)


class CheckArgs(Validate):

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '=(\w+)'
        return self.check_pattern(expression)
