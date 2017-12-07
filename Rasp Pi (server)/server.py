import socket
import time

import display

s = socket.socket()
IP = '192.168.1.102'
port = 8080
s.bind((IP,port))
s.listen(5)
print"server listening..."


while True:
    print"waiting for connection"
    conn,addr = s.accept()
    print"Got connection from", addr

    with open('received_file','wb') as f:
        print"file opened"
        #start = end = time.time()
        while True:
            #print"receiving data..."
            data = conn.recv(1024)
            #print"data=%s",data
            if not data:
                break
            #write data to a file
            f.write(data)
        #end = time.time()

    f.close()
    print"file recved"
    conn.close()
    print"connection closed"
    #break


    message = display.display()
    #time.sleep(2)
    print"Got connection from", addr
    print"sending response..."
    conn, addr = s.accept()
    conn.send(message)
    print"message sent"
    conn.close()
    #break
    
