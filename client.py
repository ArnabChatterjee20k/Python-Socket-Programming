from http import client
import socket

HEADER = 64 # 64 bytes must be the exactly length of the first message sent by the client
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.225.192"

ADDR = (SERVER , PORT)

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    # basically we will send the first which tells the size of the upcoming message . So to achieve this we are using a intger along with the space . Number of spaces will be equal to the size of the message. 
    client.send(send_length)
    client.send(message) # actual message

send("hllooo")
send("hllooo")
send(DISCONNECT_MESSAGE)