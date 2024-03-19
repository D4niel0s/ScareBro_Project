import websocket # pip install websocket-client
from datetime import datetime, timedelta

ws = websocket.WebSocket()
ws.connect("ws://192.168.200.126") # Use the IP address from the ESP32 board - printed to the serial monitor


def main():
    threshhold = timedelta(seconds=0.05)

    recieve_frame()
    lastRecieved = datetime.now()

    while(1):
        delta = datetime.now() - lastRecieved
        if(delta >= threshhold):
            recieve_frame()
            lastRecieved = datetime.now()
            print(delta)


def recieve_frame():
    ws.send("") # Triggers onWebSocketEvent() of TEXT type

    binResp = ws.recv() # receiving binary image data from camera

    with open("stream.jpg", 'wb') as f:
        f.write(binResp)


if(__name__ == '__main__'):
    main()