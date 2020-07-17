import re
import random

from serverOOP.db import ServerDB
from serverOOP.serverException import *
from serverOOP.validation import *
# Controller+Model

class AbstractModels:

    def __init__(self, request):
        self.request = request

    def parse_args(self):
        return CheckArgs(self.request[-1].split('\n')[-1])

    def parse_url(self):
        return self.request[1].split('/')[1]

    def parse_id(self):
        id = self.request[1].split('/')[2]
        return NumberField(id)

    def get(self):
        id = self.parse_id()
        if not self.select(id):
            return '404'
        return '200'

    def post(self):
        # input data
        try:
            args = self.parse_args()
            id = self.parse_id()
            message = self.save(id, args)
        except (ServerValidateError, ServerDatabaseException) as exc:
            return exc
        # TODO pass args to the instance self.intialize(args)
        # TODO validate self.validate()
        # TODO self.save()
        # TODO handle all exception here
        # define message and code that server returns
        if message:
            return f'409 {message}'  # 400 bad request; 401; 403 - permissions;
        return '200 created successfully'

    def put(self):
        # update data
        try:
            args = self.parse_args()
            id = self.parse_id()
            message = self.update(id, args)
        except (ServerValidateError, ServerDatabaseException) as exc:
            return exc
        if message:
            return f'404 {message}'  # 400 bad request; 401; 403 - permissions;
        return '201 updated successfully'

    def delete(self):
        message = self.remove(self.parse_id())
        if message:
            return f'404 {message}' # 400 bad request; 401; 403 - permissions;
        return '200'

    def save(self, id, args):
        raise NotImplemented

    def update(self, id, args):
        raise NotImplemented

    def remove(self, id):
        raise NotImplemented

    def select(self, id):
        raise NotImplemented


class UserProfile(AbstractModels):

    # TODO describe name, surname, birthday, telephone class object lvl
    # for validation. Create separate classes for validation
    # e.x name, sername = charField(class); birthday = dateField(class); telephone = phoneField(class)
    # file fields.py - class field.

    '''
    TODO
    def initialize(args):
    throw exception if args != 4
        self.name(arg[0])

    TODO
    def validate():
        for field in instance.fields:
            field.check()
    '''
    # TODO general select create update delete from db.py

    def check_data(self, args):
        #TODO parse arg requirments: count 4,
        # for fields in UserProfile: validate, field
        # TODO create own exception type and raise it
        try:
            name, surname, birthday, telephone = args
        except ValueError as exc:
            raise ServerValuesException(exc)
        errors = []
        for arg in args:
            errors.append(CharField(arg))
            errors.append(CharField(arg))
            errors.append(DateTimeField(arg))
            errors.append(TeleField(arg))
        if errors:
            return errors
        return name, surname, birthday, telephone

    def save(self, id, args):
        try:
            name, surname, birthday, telephone = self.check_data(args)
        except ValueError as exc:
            raise ServerValuesException(exc)
        try:
            ServerDB.insert(id, name, surname, birthday, telephone, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)

    def select(self, id):
        try:
            return ServerDB.select(id, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)

    def update(self, args, id):
        try:
            name, surname, birthday, telephone = self.check_data(args)
        except ValueError as exc:
            return ServerValidateError(exc)
        try:
            ServerDB.update(id, name, surname, birthday, telephone, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)

    def remove(self, id):
        try:
            ServerDB.remove(id, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)


class Companies(AbstractModels):

    def check_data(self, args):
        try:
            name, address, telephone = args
        except ValueError as exc:
            raise ServerValuesException(exc)
        errors = []
        for arg in args:
            errors.append(CharField(arg))
            errors.append(CharField(arg))
            errors.append(DateTimeField(arg))
            errors.append(TeleField(arg))
        if errors:
            return errors
        return name, address, telephone

    def save(self, id, args):
        try:
            name, address, telephone = self.check_data(args)
        except ValueError as exc:
            raise ServerValuesException(exc)
        try:
            ServerDB.insert(id, name, address, telephone, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)

    def select(self, id):
        try:
            ServerDB.select(id, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)

    def update(self, id, args):
        try:
            name, address, telephone = self.check_data(args)
        except ValueError as exc:
            raise ServerValuesException(exc)
        try:
            ServerDB.update(id, name, address, telephone, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)

    def remove(self, id):
        try:
            ServerDB.remove(id, self.__class__.__name__)
        except Exception as exc:
            raise ServerDatabaseException(exc)


class RequestPatcher:

    ROUTERS = {
        "users": UserProfile,
        "companies": Companies,
    }

    def __init__(self, request):
        self.request = self.decode_request(request)

    def __call__(self):
        handler = self.ROUTERS[self.parse_url()](self.request)  # detect non exiting url and return 404
        return self.method_dispatcher(self.parse_method(), handler)

    def decode_request(self, request):
        return request.decode('utf-8').split(' ')

    def parse_method(self):
        return self.request[0]

    def parse_url(self):
        return self.request[1].split('/')[1]

    def method_dispatcher(self, method, handler):
        try:
            method_dispatcher = {
                "POST": handler.post,
                "PUT": handler.put,
                "GET": handler.get,
                "DELETE": handler.delete,
            }
            return method_dispatcher[method]()
        except KeyError:
            raise ServerMethodException(method)
