
import socket
import pickle

HOST = '127.0.0.1'
PORT = 5001

class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

obj = DataObject("SampleData", [10, 20, 30, 40])

serialized_data = pickle.dumps(obj)
client.send(serialized_data)

print("DataObject sent to server.")
print("Name:", obj.name)
print("Values:", obj.values)

response_data = client.recv(4096)
response = pickle.loads(response_data)

print("Server response:", response)
print("Sum of values:", response["sum"])

client.close()
