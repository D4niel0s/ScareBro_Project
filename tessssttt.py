import websocket # pip install websocket-client
from PIL import Image
import socket

ws = socket.socket()
ws.connect(("192.168.200.72",80))

while(True):
    binDat = ws.recv(1000000)

    with open("STREAM.jpg",'wb') as f:
        f.write(binDat)