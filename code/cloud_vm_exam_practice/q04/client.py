import socket
HOST, PORT = "127.0.0.1", 5104
filename = input("Enter filename present in server directory: ").strip()
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(filename.encode())
    print(s.recv(4096).decode())
