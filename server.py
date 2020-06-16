import json
import socket


class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # install server socket ipv4
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse address

    def __init__(self, address, port):
        self.server_socket.bind((address, port))  # binds server to the address
        self.request = None                       # request from user
        self.storage = {}

    def run(self):
        socket_server = self.server_socket
        socket_server.listen()    # enable server socket
        while True:
            client_socket, _ = socket_server.accept()   # derive client socket [1] address
            self.request = client_socket.recv(1024)  # receive request
            response = self.make_response()          # our response to the client
            client_socket.sendall(response)          # send it to the client
            client_socket.close()

    def parse_requset(self):
        parsed = self.request.decode().split(' ')  # decode and "b'GET / = method and URL
        method = parsed[0]
        url = parsed[1]
        return method, url

    def make_response(self):
        method, url = self.parse_requset()
        headers, code = self.make_headers(method, url)
        return headers.encode()

    def dictionary(self, method=None):
        if method:
            options = {
                "POST": {'hello': 'default'},
                "PUT": {'new_key': 'hello'} if 'hello' in self.storage else {'hello': 'default'},
                "DELETE": {},
                "GET": self.storage,
            }
            self.storage = options.get(method)
            return self.storage
        return

    def urls(self):
        urls = ['/']
        return urls

    def methods(self):
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        return methods

    def make_headers(self, method, url):
        if url not in self.urls():
            return ('HTTTP/1.1 404 Not found\n\n', 404)
        if method not in self.methods():
            return ('HTTTP/1.1 405 Method not allowed\n\n', 405)
        storage = self.dictionary(method)
        return (f'HTTTP/1.1 202 response: {storage}\n\n', 202)


if __name__ == '__main__':
    a = Server('localhost', 8080)
    a.run()

#curl -X GET -d arg=val -d arg2=val2 localhost:8080