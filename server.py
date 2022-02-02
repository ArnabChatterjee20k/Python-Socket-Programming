import socket , threading

HEADER = 64 # 64 bytes must be the exactly length of the first message sent by the client
PORT = 5050
SERVER = "192.168.225.192" # using local area network ip
# print(socket.gethostname()) # DESKTOP-BMCLCFF. It is the name of my computer which represents me in the network
SERVER = socket.gethostbyname(socket.gethostname()) # getting ip address dynamically by the name of the computer
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(family = socket.AF_INET , type = socket.SOCK_STREAM)  
# AF_INET is the Internet address family for IPv4
#SOCK_STREAM means that it is a TCP socket.

#binding server to a address
server.bind(ADDR)

def handle_client(conn , addr):
    """Since this will be in new thread so this will run concurrently or paralelly for each client."""
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # this is a blocking line of code as we have to wait for the client's message. So it's must be in a new thread other than main thread so that other client are also get connected and connection isuues does not occur due to this line.
        # recv needs a buffer size or size of the message
        # here we will first receive the actual message size.
        # decoding the binary format into the provided format

        msg_length = int(msg_length) # now the msg_length will be used as the buffer size
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
        # infinite loop for listening
        print(server.accept())
        conn , addr = server.accept() # storing the connection object in conn for communication and addr if for storing address of the client. It will be ipaddress and port
        thread = threading.Thread(target=handle_client , args=(conn , addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}") # subtracting the main thread
print("[StARTING] server is starting.........")
start()