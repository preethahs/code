
import socket
import threading

lock = threading.Lock()
busy = False

def handle(c):
    global busy

    while True:
        msg = c.recv(1024).decode()

        if not msg:
            break

        if msg == "REQUEST":
            with lock:
                if not busy:
                    busy = True
                    c.send("GRANT".encode())
                else:
                    c.send("WAIT".encode())

        elif msg == "RELEASE":
            with lock:
                busy = False
                c.send("RELEASED".encode())

    c.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 12345))
s.listen(5)

print("Coordinator is ready")

while True:
    c, addr = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()
