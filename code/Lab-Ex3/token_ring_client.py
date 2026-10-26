
import socket
import time

HOST = "127.0.0.1"
PORT = 5006

name = input("Process name: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall((name + "\n").encode())

buffer = ""

print(name, "waiting for token...")

try:
    while True:
        data = client.recv(4096)
        if not data:
            break

        buffer += data.decode()

        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)

            if message == "TOKEN":
                print(name, "entered critical section")
                time.sleep(3)
                print(name, "leaving critical section")

                client.sendall(b"PASS\n")
                print(name, "passed the token")

                # Wait for the token to return in the next round.
                print(name, "waiting for token again...")

except (ConnectionError, OSError):
    print("Connection to server lost")

finally:
    client.close()
