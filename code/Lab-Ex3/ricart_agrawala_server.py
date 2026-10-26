
import socket
import threading

HOST = "127.0.0.1"
PORT = 5005

clients = {}
lock = threading.Lock()


def handle_client(conn, addr):
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
            if name in clients:
                conn.sendall(b"ERROR|Duplicate process name\n")
                return
            clients[name] = conn

        print(f"{name} connected")
        broadcast_peers()

        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message:
                    continue

                with lock:
                    recipients = [
                        c for peer, c in clients.items()
                        if peer != name
                    ]

                for recipient in recipients:
                    try:
                        recipient.sendall((message + "\n").encode())
                    except OSError:
                        pass

    except (ConnectionError, OSError):
        pass
    finally:
        if name is not None:
            with lock:
                if clients.get(name) is conn:
                    del clients[name]
            broadcast_peers()

        conn.close()


def broadcast_peers():
    with lock:
        names = sorted(clients)
        message = "PEERS|" + ",".join(names) + "\n"
        connections = list(clients.values())

    for conn in connections:
        try:
            conn.sendall(message.encode())
        except OSError:
            pass


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"Ricart-Agrawala server listening on port {PORT}")

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
