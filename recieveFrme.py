import serial # pip install pyserial
import websocket # pip install websocket-client
from datetime import datetime, timedelta

cam = websocket.WebSocket()
cam.connect("ws://192.168.200.126") # Use the IP address from the ESP32 board - printed to the serial monitor

bt = serial.Serial("COM10", 9600) # port of the connected usb module (pair with laptop first)
bt.reset_input_buffer()

def main():
    threshhold = timedelta(seconds=0.05)

    frameToFile()
    lastRecieved = datetime.now()

    while(1):
        delta = datetime.now() - lastRecieved
        if(delta >= threshhold):
            frameToFile()
            lastRecieved = datetime.now()
            #HERE GOES CALCULATION
            song = "1".encode()

            bt.write(song) #song variable is limited to one byte
            bt.reset_input_buffer() #Discard any remains of current iteration in bt connection's input buffer
    
    #Close connections to camera and to bluetooth dongle when finished
    bt.close()
    cam.close()

#Recieves a frame from cam and writes it to a file "stream.jpg" in the current directory
def frameToFile():
    cam.send("") # Triggers onWebSocketEvent() of TEXT type

    binResp = cam.recv() # receiving binary image data from camera

    with open("stream.jpg", 'wb') as f:
        f.write(binResp)


if(__name__ == '__main__'):
    main()