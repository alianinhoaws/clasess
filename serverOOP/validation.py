import re
from serverOOP.serverException import ServerValidateError, ServerValuesException


class Validate:
    """Base class for validation args from request witch based on predefined patterns."""


    def __init__(self, inputs):
        self._value = None
        self.inputs = inputs
        if inputs and isinstance(inputs, str):
            self.validate()
        else:
            raise ServerValuesException(inputs)

    @property
    def value(self):
         return str(self._value)  # decorate before give to external

    @value.setter
    def value(self, inputs):
        self._value = inputs

    def validate(self):
        pass

    def check_pattern(self, expression, pattern):
        if not re.fullmatch(expression, self.inputs):
            raise ServerValidateError(self.inputs, pattern)
        self.value = self.inputs


class CharField(Validate):
    """Validate only Char args started with lower case."""

    def __init__(self, inputs):
        super().__init__(inputs)

    def validate(self):
        expression = '[A-Z][\w]*'
        pattern = 'Azazazaz'
        return self.check_pattern(expression, pattern)


class TeleField(Validate):
    """Validate telephone number."""

    def __init__(self, inputs):
        super().__init__(inputs)

    def validate(self):
        expression = '[0-9]{10}'
        pattern = '0671230213'
        return self.check_pattern(expression, pattern)


class NameField(Validate):
    """Validate only Char args started with capital letter."""

    def __init__(self, inputs):
        super().__init__(inputs)

    def validate(self):
        expression = '[A-Z][\w]*'
        pattern = 'Name'
        return self.check_pattern(expression, pattern)


class DateTimeField(Validate):
    """Validate dates."""

    def __init__(self, inputs):
        super().__init__(inputs)

    def validate(self):
        expression = '\d{2}/\d{2}/\d{4}'
        pattern = '22/08/2010'
        return self.check_pattern(expression, pattern)


class NumberField(Validate):
    """Validate numbers."""

    def __init__(self, inputs):
        super().__init__(inputs)

    def validate(self):
        expression = '[\d]*'
        pattern = '1234567'
        return self.check_pattern(expression, pattern)


class CheckArgs(Validate):
    """Parse args in existing string."""

    def __init__(self, inputs):
        super().__init__(inputs)

    def validate(self):
        expression = '[(\w+)=(\w+)&]+'
        pattern = '"=arg1*"'
        self.check_pattern(expression, pattern)
