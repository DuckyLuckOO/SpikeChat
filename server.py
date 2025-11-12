import socket
from database.database import add_user, save_message, get_conn, list_messages_for, init_db

init_db()
s = socket.socket()
s.bind(("0.0.0.0", 5000))
s.listen(1)
print("Server ready on port 5000...")
user_ip = ""

while True:
    conn, addr = s.accept()
    user_ip, port = addr
    add_user(str(user_ip))
    
    
    # if user_ip == "127.0.0.1":
    #     break
    # else:
    #     print("Connection tried by " + user_ip + ":" + port)
    #     conn.sendall(b"You snicky spike, ain't no way you can spike our spike")
    #     conn.close()
    break

RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
RESET   = "\033[0m"

logo = rf"""
{YELLOW}
  _____       _ _          _____ _           _   
 / ____|     (_) |        / ____| |         | |  
| (___  _ __  _| | _____ | |    | |__   __ _| |_ 
 \___ \| '_ \| | |/ / _ \| |    | '_ \ / _` | __|
 ____) | |_) | |   <  __/| |____| | | | (_| | |_ 
|_____/| .__/|_|_|\_\___| \_____|_| |_|\__,_|\__|
       | |                                              
       |_|          {CYAN}💬  SpikeChat Connected  💬{RESET}
"""
print(logo + RESET)


while True:
    data = conn.recv(1024)
    if data:
        message = user_ip + " : " + data.decode()
        print("Client:", data.decode())
        conn.sendall(message.encode())
        