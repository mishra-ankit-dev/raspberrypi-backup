import time
import socket

class server():

    def __init__(self, port):
        global serversocket
        self.port = port
        #self.host = socket.gethostname()
        self.host = '10.0.0.1'
        print(self.host)
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(serversocket)  
        serversocket.bind((self.host, self.port))
        serversocket.listen(2)
        
    def __str__(self):
        print('Binding completed to:  ', self.host,':', self.port)
        print('Server listening')

    def setup_connection(self):
        while True:
            #print('Entered while loop')
            clientSocket, addr = serversocket.accept()
            print("Got a connection from", str(addr))

            msg = 'Thank you for connecting'+ "\r\n"
            clientSocket.send(msg.encode('ascii'))
            clientSocket.close()
            print('connection closed')

if __name__ =='__main__':
    try:
        s = server(12345)
        s.__str__()
        s.setup_connection()
    except KeyboardInterrupt:
        print('Closing program')
    except socket.error as err:
        print(err)
    finally:
        pass
