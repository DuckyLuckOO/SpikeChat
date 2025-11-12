import socket, threading
from database.database import add_user, save_message, get_conn, list_messages_for, init_db

clients = set()
lock = threading.Lock()

def handle_client(conn, addr):
    with conn:
        with lock: clients.add(conn)
        try:
            while True:
                data = conn.recv(4096)
                if not data:  # client closed
                    break
                msg = f"{addr[0]}: {data.decode(errors='replace')}"
                print(msg)
                # echo to the sender only:
                # conn.sendall(msg.encode())
                # OR broadcast to everyone:
                with lock:
                    dead = []
                    for c in clients:
                        try:
                            c.sendall(msg.encode())
                        except Exception:
                            dead.append(c)
                    for d in dead:
                        clients.discard(d)
        finally:
            with lock:
                clients.discard(conn)
    print(f"[disconnected] {addr}")


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
        
def main():
    s = socket.socket()
    s.bind(("0.0.0.0", 5000))
    s.listen(16)
    print(f"Server ready on 0.0.0.0:5000 ...")
    try:
        while True:
            conn, addr = s.accept()
            print(f"[connected] {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        s.close()

if __name__ == "__main__":
    main()