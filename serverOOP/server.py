import socket
from serverOOP.threadpool import ThreadPool
from serverOOP.models import RequestPatcher


class Server:
    """HTTP threads server."""

    def __init__(self, address, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.request = None

    def run(self):
        """Method to start the server, threads enabled."""
        socket_server = self.server_socket
        socket_server.listen()
        task_pool = ThreadPool()
        while True:
            client_socket, _ = socket_server.accept()
            task_pool.add_task((client_socket, self.job))

    '''
        STUB -> hardcode return value of an object
        MOCK -> create smart object e.x. if data .... return values according to the passed data
            - FAKE
            - MOCK
            -
            -
    '''

    '''
    if request not empty save_to_base
        check response data 
            "404 URL not found"
            str(ServerMethodException(method)) - > 405_Method__patch__is_not_allowed
            "200 OK"
            "201 Created",
            "204 No Content"
            "400 Bad Request"
            "404 Not Found"
            "409 Conflict"
            
        check that client_socket.sendall was called once
        check that client_socket.close was called once
    '''
    def job(self, client_socket):
        """Method to redirect received request to the model and response result to the client."""
        self.request = client_socket.recv(1024)  # TODO STUB request
        if self.request:
            response = str(RequestPatcher(request=self.request)())
            client_socket.sendall(response.encode())
            client_socket.close()


if __name__ == '__main__':
    server = Server('localhost', 8080)
    server.run()



