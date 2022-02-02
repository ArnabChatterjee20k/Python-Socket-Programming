import socket, threading

HEADER = 64
PORT = 5050
SERVER = "192.168.225.192"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# AF_INET is the Internet address family for IPv4
# SOCK_STREAM means that it is a TCP socket.

# binding server to a address
server.bind(ADDR)


def handle_client(conn, addr):
    """Since this will be in new thread so this will run concurrently or paralelly for each client."""

    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr} --> {msg}]")
    conn.close()


def start():
    """it will listen to connections and pass them to handle_client function which will run in a new thread."""
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print("[StARTING] server is starting.........")
start()
