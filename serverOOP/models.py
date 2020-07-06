import re

STORAGE = {
    'companies': {},
    'users': {},
}


class RequestPatcher:

    def __init__(self, request):
        self.request = self.decode_request(request)

    def decode_request(self, request):
        return request.decode('utf-8').split(' ')

    def parse_method(self, request):
        return request[0]

    def parse_url(self, request):
        return request[1].split('/')[1]

    def parse_args(self, request):
        return request[-1].split('\n')[-1]

    def parse_id(self, request):
        return request[1].split('/')[2]

    def save(self, request, args):
        return UserProfile(self.parse_id(request), args[0], args[1], args[2], args[3])() \
            if self.parse_url(request) == 'users' else Companies(self.parse_id(request), args[0], args[1], args[2])()

    def get(self, request):
        return STORAGE.get(self.parse_url(request), {}).get(self.parse_id(request))

    def post(self, request):
        # input data
        args = re.findall('=(\w+)', self.parse_args(request))
        if STORAGE.get(self.parse_url(request), {}).get(self.parse_id(request)):
            return
        return STORAGE.get(self.parse_url(request), {}).update({self.parse_id(request): (self.save(request, args))})

    def put(self, request):
        # update data
        if not STORAGE.get(self.parse_url(request), {}).get(self.parse_id(request)):
            return
        args = re.findall('=(\w+)', self.parse_args(request))
        return STORAGE.get(self.parse_url(request), {}).update({self.parse_id(request): (self.save(request, args))})

    def delete(self, request):
        try:
            STORAGE.get(self.parse_url(request)).pop(self.parse_id(request))
        except KeyError:
            return

    def __call__(self):
        response = self.method_dispatcher(self.parse_method(self.request))(self.request)
        print(response)
        return str(response) if response else 'OK'

    def method_dispatcher(self, method):
        try:
            method_dispatcher = {
                "POST": self.post,
                "PUT": self.put,
                "GET": self.get,
                "DELETE": self.delete,
            }
            return method_dispatcher[method]
        except KeyError as ex:
            return f'Method {ex} not allowed'


class UserProfile(RequestPatcher):

    def __init__(self, id, name, surname, birthday, telephone):
        self.id = id
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.telephone = telephone

    def __call__(self):
        return {
            'id': self.id, 'name': self.name, 'surname': self.surname,
            'birthday': self.birthday, 'telephone': self.telephone
        }


class Companies(RequestPatcher):

    def __init__(self, id, name, address, telephone):
        self.id = id
        self.name = name
        self.address = address
        self.telephone = telephone

    def __call__(self):
        return {'id': self.id, 'name': self.name, 'address': self.address, 'telephone': self.telephone}
