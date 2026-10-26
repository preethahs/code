
import socket
import pickle

HOST = '127.0.0.1'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server is waiting for a connection...")

conn, addr = server.accept()
print("Connected to:", addr)

data = conn.recv(4096)
obj = pickle.loads(data)

print("Object received:", obj.name)
print("Values:", obj.values)

total = sum(obj.values)

response = {
    "name": obj.name,
    "sum": total
}

conn.send(pickle.dumps(response))
print("Sum sent to client:", total)

conn.close()
server.close()
