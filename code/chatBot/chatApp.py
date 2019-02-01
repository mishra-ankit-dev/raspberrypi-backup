#-*- coding: UTF-8 -*-

import sys
import time
import signal
import socket
import select
import tkinter

from tkinter import *
from threading import Thread

loginTop = Tk()
loginTop.title("Login page")


def login():
    #global E1, E2
    
    L1 = Label(loginTop, text = "Username")
    L2 = Label(loginTop, text = "Password")

    L1.grid(row = 0, column = 0)
    L2.grid(row = 1, column = 0)

    E1 = Entry(loginTop, bd = 5)
    E1.grid(row = 0, column = 1)

    E2 = Entry(loginTop, bd = 5, show = '*')
    E2.grid(row = 1, column = 1)

    username = E1.get()
    password = E2.get()
    
    #args = (username, password)

    B1 = Button(loginTop, text = 'submit', command = lambda args = (username, password) : chatApp())   # chatApp(*args)
#    B1 = Button(loginTop, text = 'submit', command = chatApp(args = [username, password]))   # chatApp(*args)

    B1.grid(row = 2, column = 1)
    
    #loginTop.mainloop()

def chatApp(username = "", password = ""):
    global textBox, chatTop, msg_list
    try:
        print(username, password)
        
        if (username == "") and (password == ""):
    #    if (E1.get() == 'a') and (E2.get() == 'p'):
            loginTop.destroy()

            # Create a new Screen named chatTop
            chatTop = Tk()
            chatTop.title('chatApp')
            chatTop.geometry('500x500')
            
            msgFrame = Frame(chatTop, relief=SUNKEN)
            msgFrame.pack()
            

            # Create a scrollbar widget
            my_msg = StringVar()
            scrollbar = Scrollbar(msgFrame)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            msg_list = tkinter.Listbox(msgFrame, height=30, width=60, yscrollcommand=scrollbar.set)
            msg_list.pack(side=LEFT, fill=BOTH)  # expand = True
            
            scrollbar.config(command = msg_list.yview)
            
            # Create a text box and a send button
            textBox = Entry(chatTop, bd = 5)
            textBox.bind("<Return>", sendMessage)
            textBox.place(x = 250, y = 470)

            # Create a button named send and bind it to sendMessage()
            sendButton = Button(chatTop, text = 'send', comman = lambda event = 0 :sendMessage(event))
            sendButton.place(x = 430, y = 470)
            
            # Create menu bar
            menubar = Menu(chatTop)
                    
            # Create File as Menu in menu bar
            filemenu = Menu(menubar, tearoff = 0)
            
            # Add options to File menu
            filemenu.add_command(label="New", command = donothing)
            filemenu.add_command(label = "Open", command = donothing)
            filemenu.add_command(label = "Save", command = donothing)
            filemenu.add_command(label = "Save as...", command = donothing)
            filemenu.add_command(label = "Close", command = onExit)

            filemenu.add_separator()

            filemenu.add_command(label = "Exit", command = chatTop.destroy)
            menubar.add_cascade(label = "File", menu = filemenu)

            # Create Edit as Menu in the menu bar
            editmenu = Menu(menubar, tearoff=0)

            # Add options to Edit menu
            editmenu.add_command(label = "Undo", command = donothing)

            editmenu.add_separator()

            editmenu.add_command(label = "Cut", command = donothing)
            editmenu.add_command(label = "Copy", command = donothing)
            editmenu.add_command(label = "Paste", command = donothing)
            editmenu.add_command(label = "Delete", command = donothing)
            editmenu.add_command(label = "Select All", command = donothing)

            menubar.add_cascade(label = "Edit", menu = editmenu)

            # Create helpmenu as Menu in the menu bar
            helpmenu = Menu(menubar, tearoff=0)

            # Add options to helpmenu menu
            helpmenu.add_command(label = "Help Index", command = donothing)
            helpmenu.add_command(label = "About...", command = donothing)
            menubar.add_cascade(label = "Help", menu = helpmenu)

            # Add menubar to the top level here chatTop
            chatTop.config(menu = menubar)
            
            chatTop.mainloop()

    except KeyboardInterrupt:
        print('Quiting program')
        sys.exit()
    except Exception as e:
        print('chatApp Exception :', e)

def donothing():
    """ does nothing but creates a new window with a button """
    
    filewin = Toplevel(chatTop)
    button1 = Button(filewin, text="Do nothing button")
    button1.pack()

def onExit():
    """ After a user chooses to exit the chatroom """

    chatTop.quit()
    
    #exitTop = Toplevel()
    exitTop = Tk()
    exitTop.title("Restart")

    restartButton = Button(exitTop, text = 'RESTART', command = login)
    restartButton.pack()
    #exitTop.mainloop()
    stop = False
    
        
def sendMessage(event):
    """ Sends the message written in text box to server and prints it on chatroom """

    # Get message from the textBox and then delete it
    message = textBox.get().encode('ascii')
    textBox.delete(0, END)

    # Send it to the server
    server.send(message)

    # Print the message on sender's console
    sys.stdout.write("<You  > : ") 
    sys.stdout.write(str(message)[2:-1]) 
    sys.stdout.flush()

    # Insert message to the last of the listbox
    msg_list.insert(END, "<You  > : {}".format(str(message)[2:-1]))
    

def receiveMessage(stop = True):
    """ check is there any incoming message """

    #stop = True
    #global stop
    while stop:
    
        try:    
            # maintains a list of possible input streams 
            sockets_list = [sys.stdin, server]
            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

            for socks in read_sockets: 
                if socks == server:
                    message = socks.recv(2048).decode('ascii')
                    print(str(message)[2:])
                    msg_list.insert(END, message)
                                    
        except (KeyboardInterrupt, SystemExit):
            print("exiting")
            stop = False
            #server.close()
            #receive_thread.join()
        
def connectServer():
    """ Connects to the chatroom"""
    
    global server
    port = 12345
    host = '10.0.0.1'                           
   
    # create a socket object and connect to server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.connect((host, port))                               

        # Receive no more than 2048 bytes
        msg = server.recv(2048)                              
        print (msg.decode('ascii'))
        
    except Exception as e:
        print("exiting")
        #receive_thread.join()
        print(e)

def handler(signal, frame):
    global THREADS
    print("Ctrl-C.... Exiting")
    for t in THREADS:
        t.alive = False
    stop = False
    sys.exit()

if __name__ == '__main__' :
    try:
        connectServer()

        global THREADS
        THREADS = []
        signal.signal(signal.SIGINT, handler)
        receive_thread = Thread(target=receiveMessage)
        receive_thread.daemon=True
        receive_thread.start()
        THREADS.append(receive_thread)
        print(THREADS)
        
        login()
        loginTop.mainloop()
        
    except (KeyboardInterrupt, SystemExit):
        server.close()
        print('\n! Received keyboard interrupt, quitting threads.\n')
        
    except Exception as e:
        print("exiting")
        stop = False
        print(e)
                
    finally:
        #receive_thread.terminate()
        server.close()
        stop = False
        
