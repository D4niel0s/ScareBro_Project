# Tinker Foundry
# Using websockets with ESP32 to transfer image data...
# Reference... https://shawnhymel.com/1675/arduino-websocket-server-using-an-esp32/
# also https://www.dfrobot.com/blog-1194.html?tracking=5cc027fb1dc4e
import websocket # pip install websocket-client
import datetime

ws = websocket.WebSocket()
ws.connect("ws://192.168.200.126") # Use the IP address from the ESP32 board - printed to the serial monitor
now = datetime.now()

while(1):
    prev = now
    now = datetime.now()

    ws.send("capture") # Triggers onWebSocketEvent()

    binResp = ws.recv() # receiving binary image data from camera

    with open("stream.jpg", 'wb') as f:
        f.write(binResp)
        
    print(now-prev)

# Gracefully close WebSocket connection (Will never get here, connection will be abruptly closed when code is stopped)
ws.close()