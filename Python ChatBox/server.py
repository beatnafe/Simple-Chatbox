import socket
import threading

# Run app on local host
HOST = '127.0.0.1'
PORT = 2022

# Create a TCP Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

users = []
usernames = []


def broadcast(message):
    '''
    Sends a message to all the users that are connected to the server 

    Parameters
    ----------
    message : encoded version of a string
    '''
    for user in users:
        user.send(message)


def handle(user):
    '''
    Handles the individual connections of the clients

    Parameters
    ----------
    user : user that is logged in to the client
    '''
    while True:
        try:
            # Receive message then broadcast message to all the users that are connected
            message = user.recv(1024)
            broadcast(message)
        except:
            users.remove(user)
            user.close()
            username = usernames[users.index(user)]
            usernames.remove(username)
            break


def receive():
    '''
    Receives and accepts new clients to the server
    '''
    while True:
        user, address = server.accept()
        user.send("USER".encode('utf-8'))
        users.append(user)
        username = user.recv(1024)
        usernames.append(user)
        broadcast(f"{username} has entered the chatroom \n".encode('utf-8'))
        user.send("Connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()


receive()
