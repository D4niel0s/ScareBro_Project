import cv2 # pip install opencv-python
import serial # pip install pyserial
import websocket # pip install websocket-client
from ultralytics import YOLO # pip install ultralytics
from datetime import datetime, timedelta



# Connect to camera
cam = websocket.WebSocket()
cam.connect("ws://192.168.175.44") # Use the IP address from the ESP32 board - printed to the serial monitor
STREAM_FILENAME = "stream.jpg"
OUTPUT_FILENAME = "output.jpg"

# Connect to bluetooth dongle - connected to arduino
bt = serial.Serial("COM4", 9600) # port of the connected usb module (pair with laptop first)
bt.reset_input_buffer()

# Create a classifier object from the trained model
model = YOLO("../secondModel&stats/weights/best.pt") # Create classifier
model.to('cpu') # Model was trained on GPU so needs to be converted to cpu for detection
MIN_SCORE = 0.5 # The minimum "confidence" that we want in order to count as a classification



def main():
    threshhold = timedelta(seconds=0.05)
    lastUpdate = datetime.now()

    while(1):
        delta = datetime.now() - lastUpdate

        if(delta >= threshhold):
            recieve_frame()
            id = classify()
            sendBT(str(id))

            lastUpdate = datetime.now()

    #Close connections to camera and to bluetooth dongle when finished
    bt.close()
    cam.close()



#Recieves a frame from cam and writes it to a file [STREAM_FILENAME] in the current directory
def recieve_frame():
    cam.send("") # Triggers onWebSocketEvent() of TEXT type

    binResp = cam.recv() # receiving binary image data from camera

    with open(STREAM_FILENAME, 'wb') as f:
        f.write(binResp)

# Sends a string tro the open BT connection
def sendBT(song:str):
    bt.write(song.encode()) #song variable is limited to one byte
    bt.reset_input_buffer() #Discard any remains of current iteration in bt connection's input buffer

# Recognizes birds in [STREAM_FILENAME]
# In case of multiple birds, returns the class id of the last bird classified (We assume singular bird for simplicity of our project)
def classify():
    frame = cv2.imread(STREAM_FILENAME) 
    res = model(frame)[0] # Recognize using model
    
    class_id = 3
    # Draw a bounding box around each recognition
    for result in res.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if(score > MIN_SCORE):
            
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 5)
            cv2.putText(frame, res.names[int(class_id)].upper(), (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 5, cv2.LINE_8)
                    
    cv2.imwrite(OUTPUT_FILENAME,frame)
    print("DETECTED CLASS",int(class_id))
    return int(class_id)+1


if(__name__ == '__main__'):
    main()