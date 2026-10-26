
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5004

name = input("Process name: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall((name + "\n").encode())

buffer = ""
grant_event = threading.Event()


def receive_messages():
    global buffer

    try:
        while True:
            data = client.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                if message == "GRANT":
                    grant_event.set()

    except (ConnectionError, OSError):
        pass


threading.Thread(
    target=receive_messages,
    daemon=True
).start()

try:
    input("Press Enter to request the critical section...")
    client.sendall(b"REQUEST\n")

    grant_event.wait()

    print(name, "entered critical section")
    time.sleep(3)
    print(name, "leaving critical section")

    client.sendall(b"RELEASE\n")

finally:
    client.close()
