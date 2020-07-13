import re
import random
from serverOOP.db import insert_users, insert_companies, create_tables

STORAGE = {
    'companies': {},
    'users': {},
}


class AbstractModels:

    def __init__(self, request):
        self.request = request
        create_tables()

    def parse_args(self):
        return re.findall('=(\w+)', self.request[-1].split('\n')[-1])

    def parse_url(self):
        return self.request[1].split('/')[1]

    def parse_id(self):
        return self.request[1].split('/')[2]

    def get(self):
        id = self.parse_id()
        if not self.select(id):
            return '404'
        return '200'

    def post(self):
        # input data
        args = self.parse_args()
        id = self.parse_id()
        message = self.save(id, args)
        #message = self.save_random_id(args)
        if message:
            return f'409 {message}'
        return '200 created successfully'

    def put(self):
        # update data
        args = self.parse_args()
        id = self.parse_id()
        message = self.update(id, args)
        if message:
            return f'404 {message}'
        return '201 updated successfully'

    def delete(self):
        message = self.remove(self.parse_id())
        if message:
            return f'404 {message}'
        return '200'

    def save(self, id, args):
        raise NotImplemented

    def save_random_id(self, args):
        raise NotImplemented

    def update(self, id, args):
        raise NotImplemented

    def remove(self, param):
        raise NotImplemented

    def select(self, id):
        raise NotImplemented


class UserProfile(AbstractModels):

    def save(self, id, args):
        try:
            name, surname, birthday, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        try:
            # STORAGE['companies'][id] = {
            #      'name': name, 'surname': surname,
            #      'birthday': birthday, 'telephone': telephone
            # }
            insert_users(id, name, surname, birthday, telephone)
        except KeyError as ex:
            return f'User already exists{ex}'


    def save_random_id(self, args):
        try:
            name, surname, birthday, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        STORAGE['users'][random.randint(1, 10)] = {
            'name': name, 'surname': surname,
            'birthday': birthday, 'telephone': telephone
        }

    def select(self, id):
        try:
            return STORAGE['users']['id']
        except KeyError:
            return

    def update(self, args, id):
        try:
            name, surname, birthday, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        try:
            STORAGE['users'][id] = {
                'name': name, 'surname': surname,
                'birthday': birthday, 'telephone': telephone
            }
        except KeyError:
            return "User unregistered"

    def remove(self, param):
        try:
            del STORAGE['users'][id]
        except KeyError:
            return "User is unregistered"


class Companies(AbstractModels):

    def save(self, id, args):
        try:
            name, address, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        try:
        #     STORAGE['companies'][id] = {
        #         'name': name, 'address': address, 'telephone': telephone
        #     }
            insert_companies(id, name, address, telephone)
        except Exception as ex:
            return f'Company already exists{ex}'

    def save_random_id(self, args):
        try:
            name, address, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        STORAGE['companies'][random.randint(1, 10)] = {
                'name': name, 'address': address, 'telephone': telephone
        }

    def select(self, id):
        try:
            return STORAGE['companies']['id']
        except KeyError:
            return "Company is unregistered"

    def update(self, id, args):
        try:
            name, address, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        try:
            STORAGE['companies'][id] = {
                'name': name, 'address': address, 'telephone': telephone
            }
        except KeyError:
            return "Company is unregistered"

    def remove(self, request):
        try:
            del STORAGE['companies'][id]
        except KeyError:
            return "Company is unregistered"


class RequestPatcher:

    ROUTERS = {
        "users": UserProfile,
        "companies": Companies,
    }

    def __init__(self, request):
        self.request = self.decode_request(request)

    def __call__(self):
        handler = self.ROUTERS[self.parse_url()](self.request)
        return self.method_dispatcher(self.parse_method, handler)

    def decode_request(self, request):
        return request.decode('utf-8').split(' ')

    def parse_method(self):
        return self.request[0]

    def parse_url(self):
        return self.request[1].split('/')[1]

    def method_dispatcher(self, method, handler):
        try:
            method_dispatcher = {
                "POST": handler.post(),
                "PUT": handler.put(),
                "GET": handler.get(),
                "DELETE": handler.delete(),
            }
            return method_dispatcher[method]
        except KeyError as ex:
            return f'Method {ex} not allowed'
