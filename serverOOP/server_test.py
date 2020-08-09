import unittest
from unittest.mock import Mock, patch

from serverOOP.server import Server


class ServerTest(unittest.TestCase):

    def fake_init(obj, host, port):
        print("call fake init")

    def test_job_404(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "POST /Wrong_url/ bla bla"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"404 URL not found")
            mock_client_socket.close.assert_called()

    def test_job_200(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "POST /companies/ HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded name=CompanyX&address=London&telephone=0685930245"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"200 OK")
            mock_client_socket.close.assert_called()

    def test_job_201(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "POST /companies/ HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded name=CompanyX&address=London&telephone=0685930245"
            mock_request.decode.return_value = "PUT /companies/1 HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded name=CompanyX&address=London&telephone=0685930245"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"201 Created")
            mock_client_socket.close.assert_called()

    def test_job_400(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "PUT /companies/0111 HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded name=CompanyX&address=London&telephone=0685930245"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"400 Bad Request")
            mock_client_socket.close.assert_called()

    def test_job_404(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "GET /companies/0111 HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"404 Not Found")
            mock_client_socket.close.assert_called()

    def test_job_204(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "DELETE /companies/0111 HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"204 No Content")
            mock_client_socket.close.assert_called()


    def test_job_405(self):
        with patch.object(Server, "__init__", self.fake_init):
            server = Server('localhost', 8080)
            mock_client_socket = Mock()
            mock_request = Mock()
            mock_request.decode.return_value = "patch /companies/0111 HTTP/1.1 Host: localhost:8080 User-Agent: curl/7.64.1 Accept: */* Content-Length: 49 Content-Type: application/x-www-form-urlencoded"
            mock_client_socket.recv.return_value = mock_request
            server.job(mock_client_socket)
            mock_client_socket.sendall.assert_called_with(b"405_Method__patch__is_not_allowed")
            mock_client_socket.close.assert_called()

'''
TODO "409 Conflict"
'''



    # @patch.object(Server, "__init__", lambda obj, host, port: None)
    # '''
    #     Can written in >>patch<< decorator
    #     mock_client_socket = Mock()
    #     mock_request = Mock()
    #     mock_request.decode.return_value = "POST /Wrong_url/ bla bla"
    #     mock_client_socket.recv.return_value = mock_request'''
    # @patch
    # def test_job_404_advanced(self, mock_client_socket):
    #     server = Server('localhost', 8080)
    #     server.job(mock_client_socket)
    #     mock_client_socket.sendall.assert_called_with(b"404 URL not found")
    #     mock_client_socket.close.assert_called()
