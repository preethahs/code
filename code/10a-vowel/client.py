
import socket

s = socket.socket()
s.connect(("localhost", 5006))

word = input("Enter a word or sentence: ")
s.send(word.encode())

print("Number of distinct vowels:", s.recv(1024).decode())

s.close()
