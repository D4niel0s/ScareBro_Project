# Tinker Foundry
# Using websockets with ESP32 to transfer image data...
# Reference... https://shawnhymel.com/1675/arduino-websocket-server-using-an-esp32/
# also https://www.dfrobot.com/blog-1194.html?tracking=5cc027fb1dc4e
import websocket # pip install websocket-client
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ws = websocket.WebSocket()
ws.connect("ws://192.168.xx.xxx") # Use the IP address from the ESP32 board - printed to the serial monitor

while(1):
    # Ask the user for some input and transmit it
    str = input("Say something: ")
    if (str == "exit"):
        break
    
    # sent the input string across the socket
    ws.send(str)

    # Wait for server to respond and print it
    if (str == "capture"):
        binResp = ws.recv_frame() # receiving binary image data (we assume grey scale) from camera
        binDat = bytearray(binResp.data)

        IMG = Image.frombytes(mode='RGBA', size=len(binDat), data=binDat, decoder_name='raw')

        IMG.save("stream.jpg")

    else:
       result = ws.recv()
       print("Received: " + result)

# Gracefully close WebSocket connection
ws.close()