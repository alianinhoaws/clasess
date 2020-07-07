import socket
from threadpool import ThreadPool
from models import AbstractModels


class Server:

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, address, port):
        self.server_socket.bind((address, port))
        self.request = None

    def run(self):
        socket_server = self.server_socket
        socket_server.listen()
        task_pool = ThreadPool()
        while True:
            client_socket, _ = socket_server.accept()
            task_pool.add_task((client_socket, self.job))

    def job(self, client_socket):
        self.request = client_socket.recv(1024)
        if self.request:
            response = str(AbstractModels(request=self.request)())
            print("RESPONSE", response)
            client_socket.sendall(response.encode())
            client_socket.close()


if __name__ == '__main__':
    server = Server('localhost', 8080)
    server.run()

#curl -X POST -d id=12 -d name='companyX' -d address='London' -d telephone='001' localhost:8080/companies/12
#curl -X GET localhost:8080/companies/12
#curl -X POST -d id=1 -d name='John' -d surname='D' -d birthday='07/07/2010' -d telephone='+380671111333' localhost:8080/users/1
#curl -X GET localhost:8080/users/1
