import socket
from database.database import add_user, save_message, get_conn, list_messages_for, init_db

init_db()
s = socket.socket()
s.bind(("0.0.0.0", 5000))
s.listen(1)
print("Server ready on port 5000...")



while True:
    conn, addr = s.accept()
    ip, port = addr
    add_user(str(ip))
    
    if ip == "127.0.0.1":
        break
    else:
        print("Connection tried by " + ip + ":" + port)
        conn.sendall(b"You snicky spike, ain't no way you can spike our spike")
        conn.close()
    
print("Connected by", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Client:", data.decode())
    conn.sendall(b"Message received!")
    s.close()