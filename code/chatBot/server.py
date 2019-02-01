import socket
from threading import Thread 
server_socket = socket.socket()
port_number = 2001
server_socket.bind(('', port_number))
server_socket.listen()

conn, addr = server_socket.accept()

def receive_data():
    data = conn.recv(1000)
    print('Client:', data.decode())

def send_data():
    while True:
        user_input = input()
        conn.sendall(user_input.encode())

t = Thread(target = receive_data)
t.start()
send_data()
