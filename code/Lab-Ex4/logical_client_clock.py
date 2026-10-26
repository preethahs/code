
import socket
import threading

HOST = "127.0.0.1"
PORT = 5007

name = input("Process name: ").strip()
clock = 0
clock_lock = threading.Lock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall((name + "\n").encode())


def receive_messages():
    global clock
    buffer = ""

    try:
        while True:
            data = client.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                if not message.startswith("EVENT|"):
                    continue

                parts = message.split("|", 3)
                if len(parts) != 4:
                    continue

                _, sender, timestamp, text = parts

                with clock_lock:
                    clock = max(clock, int(timestamp)) + 1
                    current_clock = clock

                print(
                    f"\nReceived from {sender}: {text}"
                    f" | Lamport clock = {current_clock}"
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

        with clock_lock:
            clock += 1
            timestamp = clock

        message = f"EVENT|{name}|{timestamp}|{text}\n"
        client.sendall(message.encode())

        print("Sent with Lamport timestamp:", timestamp)

except (ConnectionError, OSError):
    print("Connection to server lost")

finally:
    client.close()
    print("Client disconnected")
