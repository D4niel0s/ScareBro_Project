# Tinker Foundry
# Using websockets with ESP32 to transfer image data...
# Reference... https://shawnhymel.com/1675/arduino-websocket-server-using-an-esp32/
# also https://www.dfrobot.com/blog-1194.html?tracking=5cc027fb1dc4e
import websocket # pip install websocket-client

ws = websocket.WebSocket()
ws.connect("ws://192.168.xx.xxx") # Use the IP address from the ESP32 board - printed to the serial monitor

while(1):
    # Ask the user for some input and transmit it
    str = input("Say something: ")
    if (str == "exit"):
        break
    
    # sent the input string across the socket
    ws.send(str) # Triggers onWebSocketEvent()

    # Wait for server to respond and print it
    if (str == "capture"):
        binResp = ws._recv(1000000) # receiving binary image data from camera

        with open("stream.jpg", 'wb') as f:
            f.write(binResp)

    else:
       result = ws.recv()
       print("Received: " + result)

# Gracefully close WebSocket connection
ws.close()