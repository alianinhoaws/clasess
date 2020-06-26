import socket
import time
from threading import Thread
from queue import Queue


class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # install server socket ipv4
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse address

    def __init__(self, address, port):
        self.server_socket.bind((address, port))
        self.request = None
        self.storage = {}
        self.threadPoll = []
        self.queue = Queue()

    def run(self):
        socket_server = self.server_socket
        self.create_threads()
        socket_server.listen()
        while True:
            self.client_socket, _ = socket_server.accept()
            self.queue.put(self.client_socket)
            self.worker()


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

    def worker(self, is_abort=None):
        while True:
            task = self.queue.get()
            self.job(task)
            if self.queue.empty():
                print('No sleep')
                time.sleep(5)
                print('No wake up')
                continue


    def job(self, client_socket):
            print('Job started')
            self.request = client_socket.recv(1024)
            if self.request:
                print('request')
                response = self.make_response()
                client_socket.sendall(response)
                client_socket.close()

    def create_threads(self):
        for _ in range(1, 3):
            t = Thread(target=self.worker)
            t.start()


# we start the server create workers add threads to them
if __name__ == '__main__':
    a = Server('localhost', 8080)
    a.run()

#curl -X GET -d arg=val -d arg2=val2 localhost:8080
