
import socket
import threading

HOST = "127.0.0.1"
PORT = 5008

clients = {}
lock = threading.Lock()


def send_peer_list():
    with lock:
        names = sorted(clients)
        message = "PEERS|" + ",".join(names) + "\n"
        connections = list(clients.values())

    for conn in connections:
        try:
            conn.sendall(message.encode())
        except OSError:
            pass


def handle_client(conn, addr):
    buffer = ""

    try:
        # Read the client's name, terminated by newline.
        while "\n" not in buffer:
            data = conn.recv(4096)
            if not data:
                return
            buffer += data.decode()

        name, buffer = buffer.split("\n", 1)
        name = name.strip()

        with lock:
            clients[name] = conn

        print(f"{name} connected from {addr}")
        send_peer_list()

        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message:
                    continue

                print(f"Received from {name}: {message}")

                with lock:
                    recipients = [
                        (peer, peer_conn)
                        for peer, peer_conn in clients.items()
                        if peer != name
                    ]

                for peer, peer_conn in recipients:
                    try:
                        peer_conn.sendall(
                            (message + "\n").encode()
                        )
                    except OSError:
                        print(f"Could not send to {peer}")

    except (ConnectionError, OSError):
        pass

    finally:
        with lock:
            if clients.get(name) is conn:
                del clients[name]

        conn.close()
        print(f"{name} disconnected")
        send_peer_list()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"Vector clock server listening on port {PORT}")

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
