#! python3
import select

from models import ServerStartuP as Server
from models import UserMessages as User


def main():
    while True:
        Server()

        read_sockets, _, exception_sockets = select.select(Server.sockets_list, [], Server.sockets_list)

        # Iterate over notified sockets
        for notified_socket in read_sockets:

            # If notified socket is a server socket - new connection, accept it
            if notified_socket == Server.server_socket:

                # Accept new connection
                # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                # The other returned object is ip/port set
                client_socket, client_address = Server.server_socket.accept()

                # Client should send his name right away, receive it
                user = User.receive_message(client_socket)

                # If False - client disconnected before he sent his name
                if user is False:
                    continue

                # Add accepted socket to select.select() list
                Server.sockets_list.append(client_socket)

                # Also save username and username header
                Server.clients[client_socket] = user

                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

            # Else existing socket is sending a message
            else:

                # Receive message
                message = User.receive_message(notified_socket)

                # If False, client disconnected, cleanup
                if message is False:
                    print('Closed connection from: {}'.format(Server.clients[notified_socket]['data'].decode('utf-8')))

                    # Remove from list for socket.socket()
                    Server.sockets_list.remove(notified_socket)

                    # Remove from our list of users
                    del Server.clients[notified_socket]

                    continue

                # Get user by notified socket, so we will know who sent the message
                user = Server.clients[notified_socket]

                print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                # Iterate over connected clients and broadcast message
                for client_socket in Server.clients:

                    # But don't sent it to sender
                    if client_socket != notified_socket:

                        # Send user and message (both with their headers)
                        # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:

            # Remove from list for socket.socket()
            Server.sockets_list.remove(notified_socket)

            # Remove from our list of users
            del Server.clients[notified_socket]


if __name__ == "__main__":
    main()
