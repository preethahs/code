import socket, threading

HOST, PORT = "127.0.0.1", 5105
EXPECTED_CLIENTS = 3  # Change to the number of client terminals you will run.
clients = {}
lock = threading.Lock()
token_started = False

def send_initial_token():
    global token_started
    with lock:
        if token_started or len(clients) < EXPECTED_CLIENTS:
            return
        names = sorted(clients)
        token_started = True
        first = names[0]
        clients[first].sendall(b"TOKEN\n")
        print("Initial token sent to", first)

def handle(conn, addr):
    name = None
    buffer = ""
    try:
        while "\n" not in buffer:
            data = conn.recv(1024)
            if not data: return
            buffer += data.decode()
        name, buffer = buffer.split("\n", 1)
        name = name.strip()
        with lock:
            if name in clients:
                conn.sendall(b"ERROR|duplicate name\n")
                return
            clients[name] = conn
        print(name, "connected")
        send_initial_token()
        while True:
            data = conn.recv(1024)
            if not data: break
            buffer += data.decode()
            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                if msg == "PASS":
                    with lock:
                        names = sorted(clients)
                        if name in names and names:
                            next_name = names[(names.index(name) + 1) % len(names)]
                            next_conn = clients[next_name]
                            next_conn.sendall(b"TOKEN\n")
                            print(f"Token passed from {name} to {next_name}")
    except (ConnectionError, OSError):
        pass
    finally:
        if name:
            with lock:
                if clients.get(name) is conn:
                    clients.pop(name, None)
        conn.close()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT)); server.listen()
print(f"Token Ring server on {PORT}; waiting for {EXPECTED_CLIENTS} clients")
while True:
    c, a = server.accept()
    threading.Thread(target=handle, args=(c, a), daemon=True).start()
