import sys
import socket
import pandas as pd
from threading import Thread

#server_socket = socket.socket()
#server_socket.bind(('', 8080))
#server_socket.listen()

global clients
clients = {}

class server():
    """ This class initializes the server class
    """

    def __init__(self, server_ip = '0.0.0.0', server_port = 8081):
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

        self.clients_file = '/home/pi/chatApp/client_info.csv'
        self.client_data = pd.read_csv(self.clients_file, sep = ',')
        
                

    def client_task(self, client_name, client_conn, client_addr):
        global clients
        while True:
            self.data = client_conn.recv(1000) 
            message = '{} : {}'.format(client_name, self.data.decode())
            if self.data.decode():
                [clients[client].sendall(message.encode()) for client in clients if client != client_name] 
                print(message)
                #for client in clients:
                #    if client != client_name:
                #        #print(clients)
                #        clients[client].sendall(message.encode())
                
            else:
                if client_name in clients and clients:
                    clients[client_name].close()
                    del clients[client_name]
                    print('remaining clients are : ', clients.keys())
                    
                elif not clients:
                    print('No clients left')
                    sys.exit(0)
                    #return

def main():
    while True:
        clients_list = []
        conn, addr = s.server_socket.accept()
        print('fetching name from user')
        client_login_info = conn.recv(1000).decode()
        print(client_login_info)        
        name =  client_login_info.split(',')[0].split(':')[1][1:]
        password =  client_login_info.split(',')[1].split(':')[1][1:]
                
        name_index = s.client_data[s.client_data['client_name'] == name].index.tolist()
        print(name_index)
        clients_list = s.client_data.client_name.tolist()
        print(clients_list)
        #conn.send('Confirmed'.encode())
        if name in clients_list:
            client_password = s.client_data.client_password.get_value(name_index[0])
            print(name, client_password)
            if client_password == password:
                print('Correct Password')
                conn.sendall('Confirmed'.encode())
                print('Got a connection from client :', name)
                clients[name] = conn
                t = Thread(target=s.client_task,args=(name,conn,addr))
                t.start()
            else:
                print('Invalid password')
                conn.close()
        else:
            print('Invalid name')
            conn.close()


try:
    s = server()
    main()

except KeyboardInterrupt:
    pass

