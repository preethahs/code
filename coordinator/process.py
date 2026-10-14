
import socket
import time

s = socket.socket()
s.connect(("localhost", 12345))

s.send("REQUEST".encode())
reply = s.recv(1024).decode()
print("Coordinator:", reply)

while reply == "WAIT":
    time.sleep(1)
    s.send("REQUEST".encode())
    reply = s.recv(1024).decode()
    print("Coordinator:", reply)

if reply == "GRANT":
    print("Process enters CS")
    time.sleep(2)
    print("Process releases CS")

    s.send("RELEASE".encode())
    print("Coordinator:", s.recv(1024).decode())

s.close()
