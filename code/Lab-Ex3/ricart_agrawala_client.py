
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5005

name = input("Process name: ").strip()
clock = 0
request_time = None
peers = set()
replies = set()
deferred = set()

state_lock = threading.Lock()
state_changed = threading.Condition(state_lock)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall((name + "\n").encode())


def send(message):
    client.sendall((message + "\n").encode())


def receive_messages():
    global clock, request_time
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
                    names = set(filter(
                        None, message.split("|", 1)[1].split(",")
                    ))
                    with state_changed:
                        peers.clear()
                        peers.update(names - {name})
                        state_changed.notify_all()

                elif message.startswith("REQUEST|"):
                    _, sender, timestamp = message.split("|", 2)
                    timestamp = int(timestamp)

                    with state_changed:
                        clock = max(clock, timestamp) + 1

                        # Reply if we are not requesting, or the
                        # incoming request has higher priority.
                        if (
                            request_time is None
                            or (timestamp, sender)
                            < (request_time, name)
                        ):
                            should_reply = True
                        else:
                            deferred.add(sender)
                            should_reply = False

                    if should_reply:
                        send(f"REPLY|{name}|{sender}")

                elif message.startswith("REPLY|"):
                    _, sender, target = message.split("|", 2)

                    if target == name:
                        with state_changed:
                            replies.add(sender)
                            state_changed.notify_all()

    except (ConnectionError, OSError):
        pass


threading.Thread(
    target=receive_messages,
    daemon=True
).start()

try:
    input("Press Enter to request the critical section...")

    with state_changed:
        clock += 1
        request_time = clock
        replies.clear()
        deferred.clear()
        required_peers = set(peers)
        timestamp = request_time

    send(f"REQUEST|{name}|{timestamp}")

    with state_changed:
        while not required_peers.issubset(replies):
            state_changed.wait(timeout=0.5)

    print(name, "entered critical section")
    time.sleep(3)
    print(name, "leaving critical section")

    with state_changed:
        request_time = None
        pending = list(deferred)
        deferred.clear()

    for peer in pending:
        send(f"REPLY|{name}|{peer}")

finally:
    client.close()
