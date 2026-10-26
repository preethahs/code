
import socket
import threading

HOST = "127.0.0.1"
PORT = 5007

clients = {}
lock = threading.Lock()


def handle_client(conn, addr):
    name = conn.recv(1024).decode().strip()

    with lock:
        clients[name] = conn

    print(f"{name} connected from {addr}")

    try:
        buffer = ""

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
                        (peer, client_conn)
                        for peer, client_conn in clients.items()
                        if peer != name
                    ]

                for peer, client_conn in recipients:
                    try:
                        client_conn.sendall(
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


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"Lamport clock server listening on port {PORT}")

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
