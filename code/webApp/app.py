import socket 

import select 

import sys 

from flask import Flask, render_template


app = Flask(__name__)
reload(sys)
sys.setdefaultencoding('utf8')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


#@app.route('/')
#def main():
#    return render_template('index.html')

@app.route('/')
def showSignUp():

#    if len(sys.argv) != 3: 
#
#        print "Correct usage: script, IP address, port number"
#
#        exit() 

    #IP_address = str(sys.argv[1])
    IP_address = '10.0.0.1'

    #Port = int(sys.argv[2])
    Port = 12345
    server.connect((IP_address, Port)) 

      

    #while True: 

      

        # maintains a list of possible input streams 

    sockets_list = [sys.stdin, server] 

          

    """     here are two possible input situations. Either the 

            user wants to give  manual input to send to other people, 

            or the server is sending a message  to be printed on the 

            screen. Select returns from sockets_list, the stream that 

            is reader for input. So for example, if the server wants 

            to send a message, then the if condition will hold true 

            below.If the user wants to send a message, the else 

            condition will evaluate as true
    """
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

          

    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 

            print(message) 

        else: 

            #message = sys.stdin.readline()
            message = bytes("from webserver")

            server.send(message) 

            sys.stdout.write("<You  > : ")
            sys.stdout.write(message) 

            sys.stdout.flush()
            break
                     
        server.close()

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host = '10.0.0.1', port = 8081,debug = True)
