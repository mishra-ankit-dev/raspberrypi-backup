import sys
import socket
#import pandas as pd
from threading import Thread

#server_socket = socket.socket()
#server_socket.bind(('', 8080))
#server_socket.listen()

global clients
clients = {}

class server():
    """ This class initializes the server class
    """

    def __init__(self, server_ip = '0.0.0.0', server_port = 8080):
        print('Server object created')

        if len(sys.argv) != 3: 
            print("Correct usage: script, IP address, port number")
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.server_ip = str(sys.argv[1]) 
            self.server_port = int(sys.argv[2])

        self.server_socket = socket.socket()
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()

        
                

    def client_task(self, client_name, client_conn, client_addr):
        global clients
        while True:
            self.data = client_conn.recv(1000) 
            message = '{} : {}'.format(client_name, self.data.decode())
            if self.data.decode():
                print(message)
                [clients[client].sendall(message.encode()) for client in clients if client != client_name] 
                
                #for client in clients:
                #    if client != client_name:
                #        #print(clients)
                #        clients[client].sendall(message.encode())
                
            else:
                if client_name in clients and clients:
                    del clients[client_name]
                    print('remaining clients are : ', clients.keys())
                    
                elif not clients:
                    print('No clients left')
                    sys.exit(0)
                    return

try:
    s = server()
    while True:
        conn, addr = s.server_socket.accept()
        client_login_info = conn.recv(1000)
        name =  client_login_info[client_name]
        password =  client_login_info[client_password]

        if name in 
        
        print('Got a connection from client :', name)
        clients[name.decode()] = conn
        t = Thread(target=s.client_task,args=(name.decode(),conn,addr))
        t.start()

except KeyboardInterrupt:
    pass

except:
    pass
