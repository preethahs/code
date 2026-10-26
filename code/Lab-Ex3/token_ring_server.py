
import socket
import threading

HOST = "127.0.0.1"
PORT = 5006

# Change this to the number of clients you plan to run.
EXPECTED_PROCESSES = 2

clients = {}
lock = threading.Lock()
token_started = False


def start_token_if_ready():
    global token_started

    with lock:
        if token_started or len(clients) < EXPECTED_PROCESSES:
            return

        names = sorted(clients)
        first = names[0]
        token_started = True
        conn = clients[first]

        try:
            conn.sendall(b"TOKEN\n")
            print("Initial token sent to", first)
        except OSError:
            token_started = False


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

        print(name, "connected")
        start_token_if_ready()

        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                if message == "PASS":
                    with lock:
                        names = sorted(clients)

                        if name not in names or not names:
                            continue

                        index = names.index(name)
                        next_name = names[(index + 1) % len(names)]
                        next_conn = clients[next_name]

                        try:
                            next_conn.sendall(b"TOKEN\n")
                            print(
                                "Token passed from",
                                name, "to", next_name
                            )
                        except OSError:
                            print("Failed to pass token")

    except (ConnectionError, OSError):
        pass

    finally:
        if name is not None:
            with lock:
                if clients.get(name) is conn:
                    del clients[name]

        conn.close()
        if name:
            print(name, "disconnected")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(
    f"Token Ring server listening on port {PORT}; "
    f"waiting for {EXPECTED_PROCESSES} processes"
)

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
