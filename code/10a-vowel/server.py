
import socket

s = socket.socket()
s.bind(("localhost", 5006))
s.listen()

print("Server waiting...")
c, addr = s.accept()

word = c.recv(1024).decode().lower()
vowels = set(word) & set("aeiou")

c.send(str(len(vowels)).encode())

print("Distinct vowels:", vowels)
c.close()
s.close()
