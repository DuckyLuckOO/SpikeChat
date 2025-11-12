import socket
import threading
import sys

s = socket.socket()
s.connect(("127.0.0.1", 5000))

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

def recv_loop(sock: socket.socket):
    try:
        while True:
            message = sock.recv(1024).decode()
            print(message)
    except:
        print("recv error")
    finally:
        sock.close()


def interactive_chat(sock: socket.socket):
    t = threading.Thread(target=recv_loop, args=(s,), daemon=True)
    t.start()
    try:    
        while True:
            message = input(" ---- ") 
            sock.sendall(message.encode())
    except(KeyboardInterrupt, EOFError):
        try: 
            sock.shutdown(socket.SHUT_WR)
        except OSError:
            pass
    finally:
        t.join(timeout=1)

interactive_chat(s)

