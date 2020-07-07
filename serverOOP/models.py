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
        return re.findall('=(\w+)', request[-1].split('\n')[-1])

    def parse_id(self, request):
        return request[1].split('/')[2]

    def save(self, args):
        pass

    def get(self, request):
        return STORAGE.get(self.parse_url(request), {}).get(self.parse_id(request))

    def post(self, request):
        # input data
        if STORAGE.get(self.parse_url(request), {}).get(self.parse_id(request)):
            return
        return STORAGE.get(self.parse_url(request), {}).update(
            {self.parse_id(request): (self.save(self.parse_args(request)))}
        )

    def put(self, request):
        # update data
        if not STORAGE.get(self.parse_url(request), {}).get(self.parse_id(request)):
            return
        return STORAGE.get(self.parse_url(request), {}).update({self.parse_id(request): (self.save(request))})

    def delete(self, request):
        try:
            STORAGE.get(self.parse_url(request)).pop(self.parse_id(request))
        except KeyError:
            return

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


class AbstractModels(RequestPatcher):

    def __init__(self, request):
        super().__init__(request)

    def __call__(self):
        if self.parse_url(self.request) == 'users':
            return UserProfile(self.request)()
        return Companies(self.request)()


class UserProfile(AbstractModels):

    def __init__(self, request):
        self.request = request

    def __call__(self):
        response = self.method_dispatcher(self.parse_method(self.request))(self.request)
        print(STORAGE)
        return str(response) if response else 'OK'

    def save(self, args):
        name, surname, birthday, telephone = args
        return {
            'id': self.parse_id(self.request), 'name': name, 'surname': surname,
            'birthday': birthday, 'telephone': telephone
        }


class Companies(AbstractModels):

    def __init__(self, request):
        self.request = request

    def __call__(self):
        response = self.method_dispatcher(self.parse_method(self.request))(self.request)
        print(STORAGE)
        return str(response) if response else 'OK'

    def save(self, args):
        name, surname, address, telephone = args
        return {'id': self.parse_id(self.request), 'name': name,
                'address': address, 'telephone': telephone}
