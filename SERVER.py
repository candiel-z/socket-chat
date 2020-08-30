from select import select
import socket
import sys

from settings import HOST, PORT


class TCPServer(object):
    """A class to represent a TCP server"""

    def __init__(self, host: str, port: int) -> None:
        """
        host -- server host address (IPv4 address for work in LAN)\n
        port -- server port address
        """

        self.SERVER_ADDRESS = host, port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sockets_list = [self.server_socket]    # sockets list for select()
        self.clients = {}                           # dict {client_socket: client_address}   

    def configure_server(self, backlog: int = 0) -> None:
        """Setting-up the server socket"""

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)

        try:
            self.server_socket.bind(self.SERVER_ADDRESS)
        except OSError as e:
            print(f'OSError was occured during binding:\n{e}')
            sys.exit(0)

        self.server_socket.listen(backlog)

    def serve_forever(self) -> None:
        """Serve connect-receive-send-disconnect loop"""

        print(f'Listening for connections on {self.SERVER_ADDRESS[0]}:{self.SERVER_ADDRESS[1]} . . .')

        while True:
            read_sockets, _, _ = select(self.sockets_list, [], [])

            self._read_sockets_handler(read_sockets)

    def _read_sockets_handler(self, read_sockets: list) -> None:
        """Handle accept-connection and receive-send for all read_sockets"""

        for client_socket in read_sockets:
            if client_socket == self.server_socket:
                self._accept_connection()
            else:
                data = self._receive_data(client_socket)
                self._send_data(data, client_socket)

    def _receive_data(self, client_socket: socket) -> bytes:
        """Receive data from the client socket"""

        try:
            data = client_socket.recv(1024)
        except:
            self._close_connection(client_socket)
        else:    
            print(f'Received message from {self.clients[client_socket][0]}:{self.clients[client_socket][1]}')
            return data

    def _send_data(self, data: bytes, sender_socket: socket) -> None:
        """Send data for all connected client_sockets except sender_socket"""

        for client_socket in self.clients:
            if client_socket != sender_socket and data:
                client_socket.send(data)

    def _accept_connection(self) -> None:
        """Accept a new connection"""

        client_socket, client_address = self.server_socket.accept()

        self.sockets_list.append(client_socket)
        self.clients[client_socket] = client_address

        print(f'Accepted new connection from {client_address[0]}:{client_address[1]}')

    def _close_connection(self, client_socket: socket) -> None:
        """Close the connection to the client socket"""

        print(f'Closed connection from {self.clients[client_socket][0]}:{self.clients[client_socket][1]}')

        self.sockets_list.remove(client_socket)
        del self.clients[client_socket]


if __name__ == '__main__':
    server = TCPServer(HOST, PORT)
    server.configure_server()
    server.serve_forever()
