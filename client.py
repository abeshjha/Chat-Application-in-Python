import socket 
import select
import sys
from _thread import *   
from threading import Thread      
ports = 1024  
sender = socket.socket() 
sender.connect(('127.0.0.1', ports))
print("Succesfully Connected: Register first")

def receiver_thread():
    while True:
        message = (sender.recv(ports).decode())
        if("102" in message):
            print("header length incorrect")
            print(message)
            sender.close()
            break
        else:
            print(message)
        

Thread(target = receiver_thread).start()


while True:
    to_send = input()
    if ("register" not in to_send):
        if("@"not in to_send or ":"not in to_send):
            sender.send(to_send.encode())
        else:
            username = to_send.split(':')[0]
            message = to_send.split(':')[1]
            combine = ("Send:" + username + "\n" + "Content-length:" + str(len(message)) + "\n" + message)
            sender.send(combine.encode())
    else:
        sender.send(to_send.encode())

sender.close()