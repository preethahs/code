import socket, json
HOST, PORT = "127.0.0.1", 5102
name = input("Student name: ")
marks = [float(x) for x in input("Enter marks separated by spaces (0-100): ").split()]
payload = json.dumps({"name": name, "marks": marks}).encode()
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload)
    result = json.loads(s.recv(4096).decode())
print(json.dumps(result, indent=2))
