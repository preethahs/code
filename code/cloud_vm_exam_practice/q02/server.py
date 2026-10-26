import socket, json, threading

HOST, PORT = "127.0.0.1", 5102
records = []
lock = threading.Lock()

def handle(conn, addr):
    with conn:
        data = conn.recv(4096)
        if not data:
            return
        try:
            student = json.loads(data.decode())
            name = str(student["name"])
            marks = [float(x) for x in student["marks"]]
            if not marks or any(x < 0 or x > 100 for x in marks):
                raise ValueError("Marks must be between 0 and 100")
            total = sum(marks)
            percentage = total / len(marks)
            status = "PASS" if all(x >= 40 for x in marks) else "FAIL"
            with lock:
                records.append({"name": name, "percentage": percentage})
                ordered = sorted(records, key=lambda r: r["percentage"], reverse=True)
                rank = next(i + 1 for i, r in enumerate(ordered) if r["name"] == name)
            result = {"name": name, "total": total, "maximum": 100 * len(marks),
                      "percentage": round(percentage, 2), "status": status, "rank": rank,
                      "note": "Rank is among requests received by this running server."}
        except Exception as e:
            result = {"error": str(e)}
        conn.sendall((json.dumps(result) + "\n").encode())

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT)); server.listen()
print(f"Marks server listening on {PORT}")
while True:
    c, a = server.accept()
    threading.Thread(target=handle, args=(c, a), daemon=True).start()
