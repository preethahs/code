import socket, pickle
HOST, PORT = "127.0.0.1", 5103
obj = {"name": input("Name: "), "values": [int(x) for x in input("Numbers separated by spaces: ").split()]}
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(pickle.dumps(obj))
    response = pickle.loads(s.recv(65536))  # Trusted local lab only.
print("Deserialized server response:", response)
