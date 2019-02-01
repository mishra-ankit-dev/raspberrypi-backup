# -*- coding:utf-8 -*-
import sys
import time
import signal
import socket
import select
import tkinter

from tkinter import *
from threading import Thread

class Client():
    """ This class initializes client socket
    """

    def __init__(self, server_ip = '0.0.0.0', server_port = 8081):
        
        if len(sys.argv) != 3: 
            print("Correct usage: script, IP address, port number")
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.server_ip = str(sys.argv[1]) 
            self.server_port = int(sys.argv[2])
                    
        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_ip, self.server_port))
        
        #app.login()
        #self.client_name = app.username_entry.get()
        #self.client_password = app.password_entry.get()

        #self.client_name = input('Enter NAME : ')
        #self.client_password = input('Enter PASSWORD : ')
        #print('Name :', self.client_name, 'Password :', self.client_password)
        
        #self.client_login_info = 'Name : ', self.client_name, ',', 'Password : ', self.client_password
        #self.client_login_info['client_name'] = self.client_name
        #self.client_login_info['client_password'] = self.client_password
        #print(self.client_login_info)
        #self.client_socket.sendall("".join(self.client_login_info).encode())

    def receive_data(self):
        """ Receives data continously
        """
        print('Starting receive thread')
        while True:
            self.data = self.client_socket.recv(1000)
            if self.data.decode() == 'Confirmed':
                pass
                #app.chatApp()          
            elif self.data.decode() and self.data.decode() != 'Confirmed':
                print(self.data.decode())
                app.msg_list.insert(END, self.data.decode())

            else:
                print('Server Closed', self.data)
                self.client_socket.close()
                exit(0)
                #t.join()
            
    def send_data(self, event = 0):
        """ This method sends the message to the server
        """
        global msg_list
        #while True:       # Include while loop, input() and remove chapapp lines
        #self.send_message = input()
        self.send_message = app.textBox.get().encode()
        print(self.send_message.decode())
        app.textBox.delete(0, END)
        self.client_socket.sendall(str(self.send_message)[2:-1].encode())
        print('you   :', self.send_message.decode())

        # Insert message to the last of the listbox
        app.msg_list.insert(END, "<You  > : {}".format(str(self.send_message.decode())))

    def online(self):
        pass


class App():
    """ This class creates a python app
    """
    def __init__(self):
        self.loginTop = Tk()
        self.loginTop.title("Login page")

    
    def login(self):
        print('start login')
        self.username_entry = Entry(self.loginTop, bd = 5)
        self.password_entry = Entry(self.loginTop, bd = 5, show = '*')
        self.username_label = Label(self.loginTop, text = "Username")
        self.password_label = Label(self.loginTop, text = "Password")
    
        self.username_label.grid(row = 0, column = 0)
        self.password_label.grid(row = 1, column = 0)
        self.username_entry.grid(row = 0, column = 1)
        self.password_entry.grid(row = 1, column = 1)
        
        self.client_name = ''
        self.client_password = ''
        send_button = Button(self.loginTop, text = 'submit', command = lambda args = (self.client_name, self.client_password) : self.chatApp())   # chatApp(*args)
        #send_button = Button(self.loginTop, text = 'submit', command = self.chatApp())   # chatApp(*args)

        send_button.grid(row = 2, column = 1)

    
    def chatApp(self, client_name = "", client_password = ""):
        global textBox, chatTop, msg_list
        print('Starting chatApp')
        self.client_name = self.username_entry.get()
        self.client_password = self.password_entry.get()
        self.client_login_info = 'Name : ', self.client_name, ',', 'Password : ', self.client_password       
        s.client_socket.sendall("".join(self.client_login_info).encode())
        print(self.client_login_info)
        self.Ack_message = s.client_socket.recv(1000).decode()
        print(self.Ack_message)
        #if (self.client_name == "Ankit") and (self.client_password == "amishm786@"):
        if self.Ack_message:
            self.loginTop.destroy()
            # Create a new Screen named chatTop
            self.chatTop = Tk()
            self.chatTop.title('chatApp')
            self.chatTop.geometry('500x500')
            
            self.msgFrame = Frame(self.chatTop, relief=SUNKEN)
            self.msgFrame.pack()
            

            # Create a scrollbar widget
            self.my_msg = StringVar()
            self.scrollbar = Scrollbar(self.msgFrame)
            self.scrollbar.pack(side=RIGHT, fill=Y)
            
            self.msg_list = tkinter.Listbox(self.msgFrame, height=30, width=60, yscrollcommand=self.scrollbar.set)
            self.msg_list.pack(side=LEFT, fill=BOTH)  # expand = True
            
            self.scrollbar.config(command = self.msg_list.yview)
            
            # Create a text box and a send button
            self.textBox = Entry(self.chatTop, bd = 5)
            self.textBox.bind("<Return>", s.send_data)
            self.textBox.place(x = 250, y = 470)

            # Create a button named send and bind it to sendMessage()
            self.sendButton = Button(self.chatTop, text = 'send', comman = lambda event = 0 :s.send_data(event))
            self.sendButton.place(x = 430, y = 470)
            
            # Create menu bar
            self.menubar = Menu(self.chatTop)
                    
            # Create File as Menu in menu bar
            self.filemenu = Menu(self.menubar, tearoff = 0)
            
            # Add options to File menu
            self.filemenu.add_command(label="New", command = self.donothing)
            self.filemenu.add_command(label = "Close", command = self.onExit)

            self.filemenu.add_separator()

            self.filemenu.add_command(label = "Exit", command = self.chatTop.destroy)
            self.menubar.add_cascade(label = "File", menu = self.filemenu)

            # Add menubar to the top level here chatTop
            self.chatTop.config(menu = self.menubar)
            
            self.chatTop.mainloop()

    def donothing():
        """ does nothing but creates a new window with a button
        """
    
        filewin = Toplevel(chatTop)
        button1 = Button(filewin, text="Do nothing button")
        button1.pack()

    def onExit():
        """ After a user chooses to exit the chatroom """

        self.chatTop.destroy()
        self.exitTop = Toplevel()
        self.exitTop.title("Restart")

        self.restartButton = Button(self.exitTop, text = 'RESTART')
        self.restartButton.pack()
        self.exitTop.mainloop()
        stop = False
          
        
try:
    global t
    app =App()
    s = Client()
    t = Thread(target = s.receive_data)
    t.start()
    
    app.login()
    app.loginTop.mainloop()
    #s.send_data()

except KeyboardInterrupt:
    pass

finally:
    s.client_socket.close()
    print('closed client socket')
    t.join()
    print('closed thread')
