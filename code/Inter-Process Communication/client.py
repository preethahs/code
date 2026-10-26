
import socket

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

numbers = input("Enter numbers separated by commas: ")
client.send(numbers.encode())

response = client.recv(1024).decode()
print("Server response:", response)

client.close()
