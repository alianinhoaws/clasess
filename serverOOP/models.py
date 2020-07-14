import re
import random
from serverOOP.db import insert_users, insert_companies, derive_users_from_db, derive_companies_from_db, \
    del_companies_from_db, update_companies, update_users


class AbstractModels:

    def __init__(self, request):
        self.request = request

    def parse_args(self):
        return re.findall('=(\w+)', self.request[-1].split('\n')[-1])

    def parse_url(self):
        return self.request[1].split('/')[1]

    def parse_id(self):
        id =  self.request[1].split('/')[2]
        if not re.fullmatch('[\d]*', id):
            return 'Id should contain only digits'
        return id

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

    def remove(self, id):
        raise NotImplemented

    def select(self, id):
        raise NotImplemented


class UserProfile(AbstractModels):

    def check_data(self, args):
        try:
            name, surname, birthday, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        if not re.fullmatch('[A-Z][\w]*', name):
            return 'Name should have alphabet text and starts with Capital letter'
        if not re.fullmatch('[A-Z][\w]*', surname):
            return 'Surname should have alphabet text and starts with Capital letter'
        if not re.fullmatch('\d{2}-\d{2}-\d{4}', birthday):  # add month/day check 12/31
            return 'Telephone should contain 10 digits'
        if not re.fullmatch('[0-9]{10}', telephone):
            return 'Telephone should contain 10 digits'
        return name, surname, birthday, telephone

    def save(self, id, args):
        try:
            name, surname, birthday, telephone = self.check_data(args)
        except ValueError as ex:
            return f'Unexpected args{ex}'
        try:
            insert_users(id, name, surname, birthday, telephone)
        except Exception as ex:
            return f'{ex}'

    def save_random_id(self, args):
        try:
            name, surname, birthday, telephone = self.check_data(args)
        except ValueError as ex:
            return f'Unexpected args{ex}'
        id = random.randint(1, 10)
        try:
            insert_users(id, name, surname, birthday, telephone)
        except Exception as exc:
            return f'{exc}'

    def select(self, id):
        try:
            return derive_users_from_db(id)
        except Exception as exc:
            return f'{exc}'

    def update(self, args, id):
        try:
            name, surname, birthday, telephone = self.check_data(args)
        except ValueError as ex:
            return f'Unexpected args{ex}'
        try:
            update_users(id, name, surname, birthday, telephone)
        except Exception as exc:
            return f'{exc}'

    def remove(self, id):
        try:
            del_companies_from_db(id)
        except Exception as exc:
            return f"{exc}"

class Companies(AbstractModels):

    def check_data(self, args):
        try:
            name, address, telephone = args
        except ValueError as ex:
            return f'Unexpected args{ex}'
        if not re.fullmatch('[A-Z][\w]*', name):
            return 'Name should have alphabet text and starts with Capital letter'
        if not re.fullmatch('[\w]*', address):
            return 'Adress should have alphabet text'
        if not re.fullmatch('[0-9]{10}', telephone):
            return 'Telephone should contain 10 digits'
        return name, address, telephone

    def save(self, id, args):
        try:
            name, address, telephone = self.check_data(args)
        except ValueError as ex:
            return f'{ex}'
        try:
            insert_companies(id, name, address, telephone)
        except Exception as exc:
            return f'{exc}'

    def save_random_id(self, args):
        try:
            name, address, telephone = self.check_data(args)
        except ValueError as ex:
            return f'Unexpected args{ex}'
        id = random.randint(1, 10)
        try:
            insert_companies(id, name, address, telephone)
        except Exception as ex:
            return f'{ex}'

    def select(self, id):
        try:
            derive_companies_from_db(id)
        except Exception as exc:
            return f"{exc}"

    def update(self, id, args):
        try:
            name, address, telephone = self.check_data(args)
        except ValueError as exc:
            return f'Unexpected args{exc}'
        try:
            update_companies(id, name, address, telephone)
        except Exception as exc:
            return f"{exc}"

    def remove(self, id):
        try:
            del_companies_from_db(id)
        except Exception as exc:
            return f"{exc}"


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
