
import socket
import threading

HOST = "127.0.0.1"
PORT = 5003

clients = {}
lock = threading.Lock()


def handle_client(conn, addr):
    name = None
    buffer = ""

    try:
        # Read client name, terminated by newline.
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

        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message:
                    continue

                print(f"{name}: {message}")

                with lock:
                    recipients = [
                        (peer, peer_conn)
                        for peer, peer_conn in clients.items()
                        if peer != name
                    ]

                for peer, peer_conn in recipients:
                    try:
                        peer_conn.sendall(
                            f"{name}: {message}\n".encode()
                        )
                    except OSError:
                        print(f"Failed to send to {peer}")

    except (ConnectionError, OSError):
        pass
    finally:
        if name is not None:
            with lock:
                if clients.get(name) is conn:
                    del clients[name]

        conn.close()
        if name:
            print(f"{name} disconnected")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"Message server listening on port {PORT}")

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
