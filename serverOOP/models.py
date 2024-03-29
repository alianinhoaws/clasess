from typing import Optional
from serverOOP.db_single import ServerDB
from serverOOP.serverException import *
from serverOOP.validation import *
import sqlite3


class AbstractModels:
    """Base class for all models existing parse request and CRUD mechanics."""

    def __init__(self, request):
        self.request = request
        self.db = ServerDB()
        print(self.request)
        print(self.db)

    def init_and_validate(self, args):
        index = 0
        args_dict = {}
        for name, inst in self.__class__.__dict__.items():
            if isinstance(inst, Validate.__class__):
                try:
                    inst(args[index])
                    args_dict[name] = args[index]
                    index += 1
                except ValueError as exc:
                    raise ServerValuesException(exc)
        return args_dict

    def _parse_args(self) -> tuple or str:
        try:
            args = self.request[-1].split('\n')[-1]
            CheckArgs(args)
            return re.findall('=(\w+)', args)
        except Exception as exc:
            return str(exc)

    def _parse_url(self) -> str:
        try:
            return self.request[1].split('/')[1]
        except Exception as exc:
            return str(exc)

    def _parse_id(self) -> Optional[str]:
        try:
            id = self.request[1].split('/')[2]
            if not id:
                return None
            NumberField(id)
            return id
        except Exception as exc:
            return str(exc)

    def get(self) -> tuple or str:
        id = self._parse_id()
        result = self.select(id)
        if not result:
            return self.return_codes('404')
        return self.return_codes('200'), result

    def post(self) -> str:
        """Input data into model."""
        try:
            message = self.save(
                self._parse_id(),
                self.init_and_validate(
                    self._parse_args()
                )
            )
        except (ServerValidateError, ServerDatabaseException) as exc:
            return str(exc)
        if message:
            return self.return_codes('409')  # Can be extended 400 bad request; 401; 403 - permissions;
        return self.return_codes('201')

    def put(self) -> str:
        """Update data in model."""
        try:
            message = self.update(
                self._parse_id(),
                self.init_and_validate(
                    self._parse_args()
                )
            )
        except (ServerValidateError, ServerDatabaseException) as exc:
            return str(exc)
        if message:
            return self.return_codes("404")  # 400 bad request; 401; 403 - permissions;
        return self.return_codes("200")

    def delete(self) -> str:
        """Delete data in model."""
        message = self.remove(self._parse_id())
        if message:
            return self.return_codes("404")  # 400 bad request; 401; 403 - permissions;
        return self.return_codes("200")

    def return_codes(self, code: str) -> str:
        """Code errors dispatcher."""
        try:
            return_codes = {
                "200": "200 OK",
                "201": "201 Created",
                "202": "202 Accepted",
                "204": "204 No Content",
                "400": "400 Bad Request",
                "404": "404 Not Found",
                "409": "409 Conflict",
            }
            return return_codes[code]
        except KeyError:
            raise ServerMethodException(code)

    def save(self, id: str, args: dict):
        raise NotImplemented

    def update(self, id: str, args: dict):
        raise NotImplemented

    def remove(self, id: str):
        raise NotImplemented

    def select(self, id: str):
        raise NotImplemented


class UserProfile(AbstractModels):
    """
    User model profile

    E-x:
    name: 'Name'
    surname: 'Surname'
    birthday: '22/08/2010'
    telephone: '0671230213'
    """

    name = NameField
    surname = NameField
    birthday = DateTimeField
    telephone = TeleField

    def save(self, id: str, args: list) -> None:
        """
        Save values from related args in the DB

        :param args: values sent by the client ['name', 'surname', 'birthday', 'telephone']
        :param id: id from URL
        :raise ServerValuesException, ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            return self.db.save_to_base(self.__class__.save.__name__, args, self.__class__.__name__)
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)

    def select(self, id) -> Optional[str]:
        """
        Select raw from the DB by ID

        :param id: id from URL
        :raise ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            if not id:
                id = None
            result = self.db.select(self.__class__.__name__, id)
            return result
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)

    def update(self, id: str, args: dict) -> None:
        """
        Update values from related args in the DB

        :param args: values sent by the client ['name', 'surname', 'birthday', 'telephone']
        :param id: id from URL
        :raise ServerValuesException, ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            return self.db.save_to_base(self.__class__.update.__name__, args, id, self.__class__.__name__)
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)

    def remove(self, id: str) -> None:
        """
        Remove raw from the DB by ID

        :param id: id from URL
        :raise ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            return self.db.remove(id, self.__class__.__name__)
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)


class Companies(AbstractModels):
    """
    Companies model profile

    E-x:
    name: 'Name'
    address: 'address'
    telephone: '0671230213'
    """

    name = NameField
    address = NameField
    telephone = TeleField

    def save(self, id: str, args: list) -> None:
        """
        Save values from related args in the DB

        :param args: values sent by the client ['name', 'address', 'telephone']
        :param id: id from URL
        :raise ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            return self.db.save_to_base(self.__class__.save.__name__, args, self.__class__.__name__)
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)

    def select(self, id: str) -> Optional[str]:
        """
        Select raw from the DB by ID

        :param id: id from URL
        :raise ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            if not id:
                id = None
            result = self.db.select(self.__class__.__name__, id)
            return result
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)

    def update(self, id: str, args: dict) -> None:
        """
        Update values from related args in the DB

        :param args: values sent by the client ['name', 'address', 'telephone']
        :param id: id from URL
        :raise ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
        """
        try:
            return self.db.save_to_base(self.__class__.update.__name__, args, id, self.__class__.__name__)
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)

    def remove(self, id):
        """
        Remove raw from the DB by ID

        :param id: id from URL
        :raise ServerDatabaseException or UnexpectedError
        :return: None or error message in case exception
         """
        try:
            return self.db.remove(id, self.__class__.__name__)
        except Exception as exc:
            if isinstance(exc, sqlite3.Error):
                raise ServerDatabaseException(exc)
            raise UnexpectedError(exc)


class RequestPatcher:
    """Request controller that redirects request to the existing routes."""

    __ROUTERS = {
        "users": UserProfile,
        "companies": Companies,
    }

    def __init__(self, request):
        self.request = self.__decode_request(request)

    def __call__(self):
        """Returns executed function according requests method or 404 message in case unsupported method."""
        try:
            handler = self.__ROUTERS[self.__parse_url()](self.request)
        except KeyError:
            return "404 URL not found"
        return self.__method_dispatcher(self.__parse_method(), handler)

    def __decode_request(self, request):
        """Decode method from the request."""
        return request.decode('utf-8').split(' ')

    def __parse_method(self):
        """Derives method from the request."""
        return self.request[0]

    def __parse_url(self):
        """Derives URL from the request."""
        return self.request[1].split('/')[1]

    def __method_dispatcher(self, method: str, handler: str) -> Optional[str]:
        """Returns predefined method for performing related the method used in the request or error in case exception"""
        try:
            method_dispatcher = {
                "POST": handler.post,
                "PUT": handler.put,
                "GET": handler.get,
                "DELETE": handler.delete,
            }
            return method_dispatcher[method]()
        except KeyError:
            return str(ServerMethodException(method))
