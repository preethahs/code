import socket, pickle, threading

HOST, PORT = "127.0.0.1", 5103

def handle(conn, addr):
    with conn:
        # Demonstration protocol: one serialized object per connection.
        data = conn.recv(65536)
        try:
            obj = pickle.loads(data)  # Only use pickle with trusted clients.
            result = {"received": obj, "type": type(obj).__name__}
            response = pickle.dumps(result)
            conn.sendall(response)
            print(f"Processed object from {addr}: {obj!r}")
        except Exception as e:
            conn.sendall(pickle.dumps({"error": str(e)}))

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT)); server.listen()
print(f"Serialization server listening on {PORT}")
while True:
    c, a = server.accept()
    threading.Thread(target=handle, args=(c, a), daemon=True).start()
