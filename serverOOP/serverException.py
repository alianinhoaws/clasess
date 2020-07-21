

class ServerBaseException(Exception):
    """Base class for server errors for server."""

    def __init__(self, *args):
        try:
            if args and isinstance(args[0], str):
                self.value = args[0]
        except Exception:
            raise Exception


class ServerMethodException(ServerBaseException):
    """Catcher errors in case method is not allowed by the server."""

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'405_Method__{self.value}__is_not_allowed'


class ServerValuesException(ServerBaseException):
    """Handler for errors occurred at unpacking values."""

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'{self.value}__ServerException_Not_enough_args_were_transmitted'


class ServerDatabaseException(ServerBaseException):
    """Handler expected DB errors."""

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'{self.value}__ServerDatabaseException'


class ServerValidateError(ServerBaseException):
    """Errors validation handler, value and unmatched pattern returns."""

    def __init__(self, value, pattern):
        super().__init__(value)
        self.pattern = pattern

    def __str__(self):
        return f'ServerValidateException: Value_{self.value}__unmatched__expression__{self.pattern}'


class UnexpectedError(ServerBaseException):
    """Error handler in case not expected error in the server occurred."""

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'{self.value}__Unexpected_behaviour'
