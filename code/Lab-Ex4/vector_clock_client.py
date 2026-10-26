
import socket
import threading

HOST = "127.0.0.1"
PORT = 5008

name = input("Process name: ").strip()
vector = {name: 0}
vector_lock = threading.Lock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall((name + "\n").encode())


def receive_messages():
    global vector
    buffer = ""

    try:
        while True:
            data = client.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                if message.startswith("PEERS|"):
                    peers = sorted(
                        p for p in message.split("|", 1)[1].split(",")
                        if p
                    )

                    with vector_lock:
                        for peer in peers:
                            vector.setdefault(peer, 0)
                        vector.setdefault(name, 0)
                        current = dict(vector)

                    print("Connected processes:", peers)
                    print("Current vector:", current)

                elif message.startswith("EVENT|"):
                    parts = message.split("|", 3)
                    if len(parts) != 4:
                        continue

                    _, sender, timestamp, text = parts

                    received_vector = {}
                    if timestamp:
                        for item in timestamp.split(","):
                            process, count = item.split(":", 1)
                            received_vector[process] = int(count)

                    with vector_lock:
                        for process in (
                            set(vector) | set(received_vector)
                        ):
                            vector[process] = max(
                                vector.get(process, 0),
                                received_vector.get(process, 0)
                            )

                        # Count the receipt as a new local event.
                        vector[name] = vector.get(name, 0) + 1
                        current = dict(vector)

                    print(
                        f"\nReceived from {sender}: {text}"
                        f" | Vector clock = {current}"
                    )

    except (ConnectionError, OSError):
        pass


thread = threading.Thread(
    target=receive_messages,
    daemon=True
)
thread.start()

try:
    while True:
        text = input("Message (quit to stop): ")

        if text.lower() == "quit":
            break

        with vector_lock:
            vector[name] = vector.get(name, 0) + 1
            timestamp = ",".join(
                f"{process}:{vector[process]}"
                for process in sorted(vector)
            )
            current = dict(vector)

        message = f"EVENT|{name}|{timestamp}|{text}\n"
        client.sendall(message.encode())

        print("Sent with vector timestamp:", current)

except (ConnectionError, OSError):
    print("Connection to server lost")

finally:
    client.close()
    print("Client disconnected")
