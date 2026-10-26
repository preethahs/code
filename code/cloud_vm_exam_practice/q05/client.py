import socket, time
HOST, PORT = "127.0.0.1", 5105
name = input("Process name: ").strip()
with socket.create_connection((HOST, PORT)) as s:
    s.sendall((name + "\n").encode())
    print(name, "waiting for token...")
    buffer = ""
    while True:
        data = s.recv(1024)
        if not data: break
        buffer += data.decode()
        while "\n" in buffer:
            msg, buffer = buffer.split("\n", 1)
            if msg == "TOKEN":
                print(name, "entered critical section")
                time.sleep(2)
                print(name, "leaving critical section")
                s.sendall(b"PASS\n")
                print(name, "passed token")
