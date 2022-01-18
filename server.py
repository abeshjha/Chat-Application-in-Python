import socket           
import select
import sys
from _thread import *

port = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))      
s.listen(5) 
list_of_clients = set()
registered_user = []
Dict ={}
print ("Server is up and listening")   

def clientthread(c):
    while True:
        chk = c.recv(1024).decode()
        print(chk)
        if("register" in chk):
            print("User registration message recieved")
            username = chk.split(':')[1]
            characters = "!@#$%^&*()-+?_=,<>/"
            if ((any(special in characters for special in username)) or len(username.split())>1):
                c.send('ERROR 100: Malformed username. Please try again!'.encode())
            else:
                Dict[username]= c
                print(Dict)
                registered_user.append(username)
                c.send('Username Registered: You can start sending and receiving messages'.encode())
                while True:
                    msg = c.recv(1024).decode()
                    print(msg)
                    if("@"not in msg or ":"not in msg):
                            c.send("not a valid format. Try with @<username>:message".encode())
                    else:
                        parse_username = msg.splitlines()[0]
                        parse_length = msg.splitlines()[1]
                        parse_msg = msg.splitlines()[2]
                        if(int((parse_length.split(':'))[1]) == 0 or int((parse_length.split(':'))[1]) != (len(parse_msg))):
                            c.send("ERROR 102: Header Incomplete".encode())
                        else:
                            print("Header Length match")
                            reciever=parse_username.split(':')[1]
                            target = (reciever.split('@')[1])
                            target_socket = (Dict.get(target))
                            if(reciever=="@all"):
                                for client_socket in list_of_clients:
                                    try:
                                        client_socket.send(("**BROADCAST MESSAGE by " + username + "** " + parse_msg).encode())
                                    except:
                                        c.send(("One or more users offline. Not braodcasted to everyone.Try again").encode())
                                        print("One or more users went offline.")
                            else:
                                
                                if(target in registered_user):
                                    combine = ("Forward:" + target + "\n" + parse_length + "\n" + parse_msg)
                                    print("-----sending to recipent----")
                                    print(combine)
                                    try:
                                        target_socket.send(("MSG FROM: @"+username+": "+parse_msg).encode())
                                        c.send('User online.Message sent'.encode()) 
                                    except:
                                        c.send(("ERROR: Unable to send, user offline").encode())
                                        print("User offline.")                                   
                                    

                                else:
                                    c.send('ERROR 101! User not Registered'.encode())
        else:
            c.send('ERROR 101: Please register first'.encode())

while True:
    c, addr = s.accept()
    list_of_clients.add(c)
    print (addr[0] + " connected")
    print("List of online users:")
    print(registered_user)
    start_new_thread(clientthread,(c,))  

c.close()
s.close()