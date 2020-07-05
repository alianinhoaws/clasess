
class Entities:

    def __init__(self, request):
        method = request[0]
        self.method_dispatcher[method](self, request)

    def save(self, *args, **kwargs):
        pass

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    method_dispatcher = {
        "POST": post,
        "PUT": put,
        "GET": get,
        "DELETE": delete,
    }


class UserProfile(Entities):

    def __init__(self, id, name, surname, birthday, telephone, request):
        super().__init__(request)
        self.id = id
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.telephone = telephone


class Companies(Entities):

    def __init__(self, id, name, addr, telephone, request):
        super().__init__(request)
        self.id = id
        self.name = name
        self.address = addr
        self.telephone = telephone
