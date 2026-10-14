
import socket
import sys
import time
import threading

pid = int(sys.argv[1])
ports = {1: 5001, 2: 5002, 3: 5003}

next_id = pid % 3 + 1
next_port = ports[next_id]


def send_token():
    while True:
        try:
            s = socket.socket()
            s.connect(("localhost", next_port))
            s.send("TOKEN".encode())
            s.close()
            break
        except OSError:
            time.sleep(1)


def handle():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", ports[pid]))
    server.listen(5)

    print("Process", pid, "is ready")

    while True:
        c, addr = server.accept()
        msg = c.recv(1024).decode()
        c.close()

        if msg == "TOKEN":
            print("Process", pid, "received token")
            print("Process", pid, "enters CS")
            time.sleep(1)
            print("Process", pid, "releases CS")
            send_token()
            print("Token passed to Process", next_id)


threading.Thread(target=handle, daemon=True).start()

if pid == 1:
    time.sleep(3)
    print("Process 1 starts with the token")
    print("Process 1 enters CS")
    time.sleep(1)
    print("Process 1 releases CS")
    send_token()
    print("Token passed to Process 2")

while True:
    time.sleep(1)
