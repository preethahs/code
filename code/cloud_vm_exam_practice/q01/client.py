import socket

HOST, PORT = "127.0.0.1", 5101
with socket.create_connection((HOST, PORT)) as s:
    print(s.recv(1024).decode().strip())
    while True:
        msg = input("Message (quit to stop): ")
        s.sendall((msg + "\n").encode())
        reply = s.recv(1024).decode().strip()
        print(reply)
        if msg.lower() == "quit":
            break
