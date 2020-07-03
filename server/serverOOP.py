import socket
from threadpool import ThreadPool
from userProfile import UserProfile
from companies import Companies


class Server:

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, address, port):
        self.server_socket.bind((address, port))
        self.request = None
        self.storage = {'companies': {}, 'users': {}}

    def run(self):
        socket_server = self.server_socket
        socket_server.listen()
        task_pool = ThreadPool()
        while True:
            client_socket, _ = socket_server.accept()
            task_pool.add_task((client_socket, self.job))

    def parse_request(self):
        parsed = self.request.decode('utf-8').split(' ')  # decode and "b'GET / = method and URL
        method = parsed[0]
        url = parsed[1]
        try:
            id = (url.split('/'))[2]
        except IndexError:
            return method, url
        return method, url, id

    def make_response(self):
        method, url, id = self.parse_request()
        headers = self.make_headers(method, url, id)
        return headers.encode()

    def aggregate(self, url, data, id):
        if url.startswith('/user/'):
            try:
                name, surname, birthday, telephone = data
                self.storage.get('users').update({id: UserProfile(id, name, surname, birthday, telephone)})
                return 'OK', data
            except TypeError:
                return data
        elif url.startswith('/company/'):
            try:
                name, addr, telephone = data
                self.storage.get('companies').update({id: UserProfile(id, name, addr, telephone)})
                return 'OK', data
            except TypeError:
                return data
        else:
            return f'url {url} not found, 404'

    def post(self, tag):
        if tag:
            return 'Josef', 'Ma', '1/23/1980', '+095132354'
        return 'Garbage', 'UK', '+3831309333'

    def put(self, tag):
        print('IN PUT')
        if tag:
            return 'Josef', 'Ma', '1/23/1980', '+095132354'
        return 'Garbage', 'UK', '+3831309333'

    def delete(self, tag, id):
        print('IN DELETE')
        # try:
        #     if tag:
        #         return self.storage.get('users').pop(id)
        #     self.storage.get('companies').pop(id)
        # except KeyError:
        #     return

    def get(self, tag, id):
        print('IN GET')
        if tag:
            return self.storage.get('users', {}).get(id)
        return self.storage.get('companies', {}).get(id)

    def methods(self, method, url, id):
        tag = None
        print("METHOD", method)
        if url.startswith('/user/'):
            tag = 'User'
        methods_dict = {
                "POST": self.post(tag),
                "PUT": self.put(tag),
                "DELETE": self.delete(tag, id),
                "GET": self.get(tag, id),
            }
        try:
            return methods_dict[method]
        except KeyError as ex:
            return f'Method {ex} not allowed'

    def make_headers(self, method, url, id):
        data = self.methods(method, url, id)
        response = self.aggregate(url, data, id)
        return f'response: {response} 200\n\n'

    def job(self, client_socket):
        self.request = client_socket.recv(1024)
        if self.request:
            response = self.make_response()
            print('response', response)
            client_socket.sendall(response)
            client_socket.close()


if __name__ == '__main__':
    a = Server('localhost', 8080)
    a.run()

#curl -X GET -d arg=val -d arg2=val2 localhost:8080