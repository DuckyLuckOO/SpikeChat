import socket

s = socket.socket()
s.connect(("127.0.0.1", 5000))

s.sendall(b"Hello server!")
print(s.recv(1024).decode())
s.close()

