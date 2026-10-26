import socket
import threading

HOST, PORT = "127.0.0.1", 5101

def handle(conn, addr):
    with conn:
        conn.sendall(b"Connected to server. Type a message.\n")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            print(f"{addr}: {message}")
            if message.lower() == "quit":
                conn.sendall(b"Goodbye\n")
                break
            conn.sendall(f"Server received: {message}\n".encode())

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on {HOST}:{PORT}")
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
