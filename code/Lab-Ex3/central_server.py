
import socket
import threading

HOST = "127.0.0.1"
PORT = 5004

clients = {}
queue = []
current = None
lock = threading.Lock()


def grant_next():
    global current

    with lock:
        if current is None and queue:
            name = queue.pop(0)
            conn = clients.get(name)

            if conn is None:
                return

            current = name

            try:
                conn.sendall(b"GRANT\n")
                print("Granted critical section to", name)
            except OSError:
                current = None


def handle_client(conn, addr):
    global current
    name = None
    buffer = ""

    try:
        while "\n" not in buffer:
            data = conn.recv(4096)
            if not data:
                return
            buffer += data.decode()

        name, buffer = buffer.split("\n", 1)
        name = name.strip()

        with lock:
            clients[name] = conn

        print(name, "connected")

        while True:
            if "\n" not in buffer:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                if message == "REQUEST":
                    with lock:
                        if (
                            name != current
                            and name not in queue
                            and name in clients
                        ):
                            queue.append(name)

                    grant_next()

                elif message == "RELEASE":
                    with lock:
                        if current == name:
                            current = None

                    grant_next()

    except (ConnectionError, OSError):
        pass

    finally:
        if name is not None:
            with lock:
                if clients.get(name) is conn:
                    clients.pop(name, None)

                if name in queue:
                    queue.remove(name)

                if current == name:
                    current = None

        conn.close()
        if name:
            print(name, "disconnected")

        grant_next()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"Central coordinator listening on port {PORT}")

try:
    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()
except KeyboardInterrupt:
    print("\nServer stopped")
finally:
    server.close()
