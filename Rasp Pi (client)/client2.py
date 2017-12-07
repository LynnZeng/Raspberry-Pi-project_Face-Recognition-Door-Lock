import socket                   # Import socket module
def recv():
    s = socket.socket()             # Create a socket object
    IP = '192.168.1.102'     # Get local machine name
    port = 8080   


#ss = socket.socket()
    print"new connection"
    s.connect((IP,port))
    message = s.recv(1024)
    print"message recved:",message
    s.close()
    print"connection closed"
    return message

