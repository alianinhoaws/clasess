import re
from serverOOP.serverException import ServerValidateError, ServerValuesException


class Validate:
    """Base class for validation args from request witch based on predefined patterns."""
    #TODO
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
    """Validate only Char args started with lower case."""

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[A-Z][\w]*'
        pattern = 'Azazazaz'
        return self.check_pattern(expression, pattern)


class TeleField(Validate):
    """Validate telephone number."""

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[0-9]{10}'
        pattern = '0671230213'
        return self.check_pattern(expression, pattern)


class NameField(Validate):
    """Validate only Char args started with capital letter."""

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[A-Z][\w]*'
        pattern = 'Name'
        return self.check_pattern(expression, pattern)


class DateTimeField(Validate):
    """Validate dates."""

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '\d{2}/\d{2}/\d{4}'
        pattern = '22/08/2010'
        return self.check_pattern(expression, pattern)


class NumberField(Validate):
    """Validate numbers."""

    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '[\d]*'
        pattern = '1234567'
        return self.check_pattern(expression, pattern)


class CheckArgs(Validate):
    """Define args in existing string."""
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        expression = '=(\w+)'
        pattern = '[arg 1]*'
        return self.check_pattern(expression, pattern)

