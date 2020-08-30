import socket
import sys


class ClientSocket(object):
    """A class to represent a client socket"""

    def __init__(self, server_host: str, server_port: int) -> None:
        """Create the client socket"""

        self.SERVER_ADDRESS = server_host, server_port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def configure_socket(self) -> None:
        """Socket connection setting-up"""
        
        self.client_socket.setblocking(True)

    def connect(self):
        """Connect to the server"""

        print('Connecting . . .')
        while True:
            try: 
                self.client_socket.connect(self.SERVER_ADDRESS)
            except: 
                print('\rCan`t connect to the server', end='')
            else: 
                print('\rConnected!', end='\t\t\t\t\n')
                break

    def send(self, message: str) -> None:
        """Send message to server socket"""

        if message:
            self.client_socket.send(message.encode('utf-8'))

    def read(self) -> str:
        """Return the message recieved from the server"""

        try:
            return self.client_socket.recv(1024).decode('utf-8')
        except:
            print('Connection closed by the server')
            sys.exit(0)
