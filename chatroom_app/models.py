#! python3

"""
    Models for server and client.
    """

import socket


class ServerStartuP:
    def __init__(self, IP, PORT, server_socket, clients, socket_list):
        self.IP = '127.0.0.1'
        self.PORT = 1234
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # List of sockets for select.select()
        self.socket_list = [self.server_socket]
        self.clients = {}

        # SO_ - socket option
        # SOL_ - socket option level
        # Sets REUSEADDR (as a socket option) to 1 on socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind, so server informs operating system that it's going to use given IP and port
        # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
        self.server_socket.bind((self.IP, self.PORT))

        # This makes server listen to new connections
        self.server_socket.listen()

        print(f'Listening for connections on {self.IP}:{self.PORT}...')


class ClientStartup(ServerStartuP):
    def __init__(self, name, client_socket):
        self.name = input('Username: ')
        """ Create a socket
            socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
            socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port in server
        self.client_socket.connect((self.IP, self.PORT))

        # Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
        self.client_socket.setblocking(False)


class UserMessages(ServerStartuP, ClientStartup):
    def __init__(self, username, HEADER_LENGTH):
        self.username = self.name
        self.HEADER_LENGTH = 10

    # We need to encode username and or messages to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    def encode_message(self, message):
        self.message = message.encode('utf-8')
        header = f"{len(self.message):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(header + self.message)

    def send_username(self):
        return self.encode_message(self.username)

    # Handles message receiving
    def received_message(self, client_socket):
        try:

            # Receive our "header" containing message length, it's size is defined and constant
            message_header = self.client_socket.recv(self.HEADER_LENGTH)

            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(message_header):
                return False

            # Convert header to int value
            message_length = int(message_header.decode('utf-8').strip())

            # Return an object of message header and message data
            context = {'header': message_header, 'data': client_socket.recv(message_length)}
            return context

        except:  # noqa
            """ If we are here, client closed connection violently, for example by pressing ctrl+c on his script
             or just lost his connection
             socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
             and that's also a cause when we receive an empty message"""
            return False

    def send_message(self, message):
        self.message = input(f'{self.username} > ')
        # If message is not empty - send it
        if self.message:

            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            self.encode_message(self.message)
