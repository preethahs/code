import socket, os, threading

HOST, PORT = "127.0.0.1", 5104
BASE_DIR = os.path.abspath(".")

def handle(conn, addr):
    with conn:
        filename = conn.recv(4096).decode().strip()
        safe_name = os.path.basename(filename)
        path = os.path.join(BASE_DIR, safe_name)
        if not safe_name or not os.path.isfile(path):
            conn.sendall(b"ERROR: File not found in server directory")
            return
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        result = (f"Filename: {safe_name}\n"
                  f"Lines: {len(content.splitlines())}\n"
                  f"Words: {len(content.split())}\n"
                  f"Size: {os.path.getsize(path)} bytes")
        conn.sendall(result.encode())
        print(f"Stats sent for {safe_name} to {addr}")

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT)); server.listen()
print(f"File statistics server on {PORT}; directory: {BASE_DIR}")
while True:
    c, a = server.accept()
    threading.Thread(target=handle, args=(c, a), daemon=True).start()
