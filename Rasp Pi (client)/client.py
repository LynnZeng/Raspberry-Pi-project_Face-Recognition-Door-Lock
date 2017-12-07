import socket                   # Import socket module
import client2

def send():
    s = socket.socket()             # Create a socket object
    IP = '192.168.1.102'     # Get local machine name
    port = 8080             # Reserve a port for your service.

    s.connect((IP, port))
#s.send("Hello server!")

    while True:
        filename='/home/pi/project/capture.pgm'
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           s.send(l)
           #print('Sent ',repr(l))
           l = f.read(1024)
        f.close()
        print('Done sending')
        s.close()
        print"connection closed"
        break
#s.close()
#print"start recving"
#message = s.recv(1024)
#print"message recved:",message
    return client2.recv()
    #execfile("/home/pi/project/client2.py")
#s.close()
#print"connection closed"


