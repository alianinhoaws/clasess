import socket
import time
from threading import Thread
from queue import Queue


class Worker(Thread):

    def __init__(self, name, tasklist):
        Thread.__init__(self)
        self.name = name
        self.tasklist = tasklist

    def run(self):
        while True:
            task, job = self.tasklist.get()
            job(task)
            if self.tasklist.empty():
                time.sleep(1)


class ThreadPool:
    def __init__(self):
        self.__task_list = Queue()
        self.worker_list = [Worker(i, self.__task_list) for i in range(1, 5)]
        for worker in self.worker_list:
            worker.start()

    def add_task(self, task):
        self.__task_list.put(task)


class Server:

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, address, port):
        self.server_socket.bind((address, port))
        self.request = None
        self.storage = {}

    def run(self):
        socket_server = self.server_socket
        socket_server.listen()
        task_pool = ThreadPool()
        while True:
            client_socket, _ = socket_server.accept()
            task_pool.add_task((client_socket, self.job))

    def parse_requset(self):
        parsed = self.request.decode('utf-8').split(' ')  # decode and "b'GET / = method and URL
        method = parsed[0]
        url = parsed[1]
        return method, url

    def make_response(self):
        method, url = self.parse_requset()
        headers = self.make_headers(method, url)
        return headers.encode()

    def urls(self):
        urls = ['/']
        return urls

    def post(self):
        self.storage.update({'hello': 'default'})
        return self.storage

    def put(self):
        self.storage.update({'new_key': 'hello'} if 'hello' in self.storage else {'hello': 'default'})
        return self.storage

    def delete(self):
        self.storage = dict()
        return self.storage

    def get(self):
        return self.storage

    def methods(self, method):
        methods = {
                "POST": self.post(),
                "PUT": self.put(),
                "DELETE": self.delete(),
                "GET": self.get(),
            }
        try:
            return methods[method]
        except KeyError as ex:
            return f'Method {ex} not allowed'

    def make_headers(self, method, url):
        if url not in self.urls():
            return 'Not found 404\n\n'
        header = self.methods(method)
        if not header:
            return f'{header} 405\n\n'
        return f'response: {self.storage}, {header} 200\n\n'


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
