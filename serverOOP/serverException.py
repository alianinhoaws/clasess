

class ServerBaseException(Exception):

    def __init__(self, *args):
        try:
            if args and isinstance(args[0], str):
                self.value = args[0]
        except Exception:
            raise Exception


class ServerMethodException(ServerBaseException):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'405_Method__{self.value}__is_not_allowed'


class ServerValuesException(ServerBaseException):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'{self.value}__ServerException_Not_enough_args_were_transmitted'


class ServerDatabaseException(ServerBaseException):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f'{self.value}__ServerDatabaseException'


class ServerValidateError(ServerBaseException):

    def __init__(self, value, pattern):
        super().__init__(value)
        self.pattern = pattern

    def __str__(self):
        return f'ServerValidateException: Value_{self.value}__unmatched__expression__{self.pattern}'
