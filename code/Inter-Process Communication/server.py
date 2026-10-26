
import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server is waiting for a connection...")

conn, addr = server.accept()
print("Connected to:", addr)

data = conn.recv(1024).decode()
print("Received from client:", data)

numbers = list(map(int, data.split(',')))
total = sum(numbers)

response = f"Sum of numbers = {total}"
conn.send(response.encode())

print("Response sent to client.")

conn.close()
server.close()
