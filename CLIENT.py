from threading import Thread

from client import ClientSocket
from settings import HOST, PORT


class Client(object):
    def __init__(self, server_host: str, server_port: int) -> None:
        """
        server_host -- server host address\n
        server_port -- server port address
        """

        self.client_socket = ClientSocket(server_host, server_port)

    def configure_client(self) -> None:
        """Setting-up client-server connection"""

        self.client_socket.configure_socket()
        self.client_socket.connect()

    def serve_forever(self):
        """Serve read-send loop"""

        self._reading_handler()
        self._input() 

    def _reading_handler(self) -> None:
        """Handle reading loop"""

        Thread(target=self._reading, daemon=True).start()

    def _reading(self) -> None:
        """Print read message loop"""

        while True:
            message = self.client_socket.read()
            if message:
                print(message)

    def _input_handler(self) -> None:
        """Not used. Reserved"""

        Thread(target=self._input, daemon=True).start()

    def _input(self) -> None:
        """Send-input-message loop"""

        while True:
            self.client_socket.send(input())
        

if __name__ == '__main__':
    client = Client(HOST, PORT)
    client.configure_client()
    client.serve_forever()
