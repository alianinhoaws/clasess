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

'''
TODO 405_Method__patch__is_not_allowed def test_job_405(self):
TODO "200 OK" test_job_200(self):
TODO "201 Created",
TODO "204 No Content"
TODO "400 Bad Request"
TODO "404 Not Found"
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
