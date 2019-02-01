import socket
from threading import Thread

client_socket = socket.socket()
client_socket.connect(('localhost', 2000))

def receive_data():
    data = client_socket.recv(1000)
    print('server:', data.decode())

def sending_data():
    while True:
        user_input = input()
        client_socket.sendall(user_input.encode())


t = Thread(target = receive_data)
t.start()
sending_data()

