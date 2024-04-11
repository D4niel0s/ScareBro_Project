import serial
import websocket # pip install websocket-client
from datetime import datetime, timedelta

cam = websocket.WebSocket()
cam.connect("ws://192.168.200.126") # Use the IP address from the ESP32 board - printed to the serial monitor

bt = serial.Serial("COM10", 9600)
bt.flushInput()

def main():
    threshhold = timedelta(seconds=0.05)

    recieve_frame()
    lastRecieved = datetime.now()

    while(1):
        delta = datetime.now() - lastRecieved
        if(delta >= threshhold):
            recieve_frame()
            lastRecieved = datetime.now()
            #HERE GOES CALCULATION
            song = "1".encode()

            bt.write(song)
    
    bt.close()
    cam.close()


def recieve_frame():
    cam.send("") # Triggers onWebSocketEvent() of TEXT type

    binResp = cam.recv() # receiving binary image data from camera

    with open("stream.jpg", 'wb') as f:
        f.write(binResp)


if(__name__ == '__main__'):
    main()