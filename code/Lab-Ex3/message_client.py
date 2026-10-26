
import socket
import threading

HOST = "127.0.0.1"
PORT = 5003

name = input("Process name: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall((name + "\n").encode())


def receive_messages():
    buffer = ""

    try:
        while True:
            data = client.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                print("\nReceived:", message)

    except (ConnectionError, OSError):
        pass


threading.Thread(
    target=receive_messages,
    daemon=True
).start()

try:
    while True:
        message = input("Message (quit to stop): ")

        if message.lower() == "quit":
            break

        client.sendall((message + "\n").encode())

finally:
    client.close()
    print("Client disconnected")
