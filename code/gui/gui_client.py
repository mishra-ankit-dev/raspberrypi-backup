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
            print("Correct usage: script, IP address, Port number")
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.server_ip = str(sys.argv[1]) 
            self.server_port = int(sys.argv[2])
                    
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        
    def receive_data(self):
        """ Receives data continously
        """
        try:
            while True:
                self.data = self.client_socket.recv(1000)
                if self.data.decode() and (self.data.decode() != 'Confirmed'):
                    print(self.data.decode())
                    app.msg_list.insert(END, self.data.decode())

                elif self.data.decode() == 'Confirmed':
                    print('Received confirmaion from server')
                    self.Ack_message = self.data
                else:
                    app.login_top.destroy()
                    break
        except Exception as e:
            pass
        except KeyboardInterrupt:
            pass
        
    def send_data(self, event = 0):
        """ This method sends the message to the server
        """
        try:
            self.send_message = app.text_box.get().encode()
            #print(self.send_message.decode())
            self.client_socket.sendall(str(self.send_message)[2:-1].encode())
            print('you   :', self.send_message.decode())

            # Insert message to the last of the listbox
            app.msg_list.insert(END, "<You  > : {}".format(str(self.send_message.decode())))
            app.text_box.delete(0, END)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print('Exception :', e)
            pass
        
class App(Client):
    """ This class creates a python app
    """
    def __init__(self):
        self.login_top = Tk()
        self.login_top.title("Login page")
        self.username_entry = Entry(self.login_top, bd = 5)
        self.password_entry = Entry(self.login_top, bd = 5, show = '*')
        self.username_label = Label(self.login_top, text = "Username")
        self.password_label = Label(self.login_top, text = "Password")
    
    
    def login(self):
        try:     
            self.username_label.grid(row = 0, column = 0)
            self.password_label.grid(row = 1, column = 0)
            self.username_entry.grid(row = 0, column = 1)
            self.password_entry.grid(row = 1, column = 1)
            
            self.client_name = ''
            self.client_password = ''
            send_button = Button(self.login_top, text = 'submit', command = lambda args = (self.client_name, self.client_password) : self.chatApp())   # chatApp(*args)
            self.password_entry.bind("<Return>", s.send_data)
            send_button.grid(row = 2, column = 1)
        except Exception as e:
            pass
        except KeyboardInterrupt:
            pass
            
    def chatApp(self, client_name = "", client_password = ""):
        try:
            self.client_name = self.username_entry.get()
            self.client_password = self.password_entry.get()
            self.client_login_info = '{},{}'.format(self.client_name, self.client_password)
            s.client_socket.sendall("".join(self.client_login_info).encode())
            print('Sent login data to server',self.client_login_info)
            time.sleep(0.15)
            if s.Ack_message.decode() == 'Confirmed':
                self.chatAppGUI()
                self.chat_top.mainloop()
            else:
                self.signUpGUI()
        except Exception as e:
            pass
        except KeyboardInterrupt:
            pass
        
    def chatAppGUI(self):
        self.login_top.destroy()
                
        # Create a new Screen named chat_top
        self.chat_top = Tk()
        self.chat_top.title('chatApp')
        self.chat_top.geometry('500x500')

        # Create a message frame to contain other widgets
        self.msg_frame = Frame(self.chat_top, relief=SUNKEN)
        self.msg_frame.pack()

        # Create a scrollbar widget
        self.scrollbar = Scrollbar(self.msg_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Create a listbox to store multiple line text
        self.msg_list = tkinter.Listbox(self.msg_frame, height=30, width=60, yscrollcommand=self.scrollbar.set)
        self.my_msg = StringVar()
        self.msg_list.pack(side=LEFT, fill=BOTH)  # expand = True

        self.scrollbar.config(command = self.msg_list.yview)
                
        # Create a text box and a send button
        self.text_box = Entry(self.chat_top, bd = 5)
        self.text_box.bind("<Return>", s.send_data)
        self.text_box.place(x = 250, y = 470)

        # Create a button named send and bind it to sendMessage()
        self.send_button = Button(self.chat_top, text = 'send', command= lambda event = 0 :s.send_data(event))
        self.send_button.place(x = 430, y = 470)
                
        # Create menu bar
        self.menubar = Menu(self.chat_top)
                        
        # Create File as Menu in menu bar
        self.filemenu = Menu(self.menubar, tearoff = 0)
                
        # Add options to File menu
        self.filemenu.add_command(label="Chat", command = self.donothing)
        self.filemenu.add_command(label = "Online", command = self.online)

        self.filemenu.add_separator()

        self.filemenu.add_command(label = "Exit", command = self.chat_top.destroy)
        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        # Add menubar to the top level here chatTop
        self.chat_top.config(menu = self.menubar)

    def signUpGUI(self):
        pass

    def donothing(self):
        """ Does nothing but creates a new window with a button
        """
        filewin = Toplevel()
        button1 = Button(filewin, text="Do nothing button")
        button1.pack()

    def online(self):
        """ After a user chooses to exit the chatroom
        """
        self.online_top = Toplevel()
        self.online_top.title("Online")

        
        self.online_top.mainloop()  
        
if __name__ == '__main__':
    try:
        global t, app
        
        s = Client()
        app =App()
        t = Thread(target = s.receive_data)
        t.start()
        
        app.login()
        app.login_top.mainloop()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
    finally:
        s.client_socket.close()
        print('closed client socket')
        
