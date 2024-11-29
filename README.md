# Final project - ScareBro™

This project is made as a high school final project. </br>
<b>Project's goals: Identify incoming birds and scare them away using sound - to save them from certain death via wind turbines.</b>

## Project's hardware components

* ESP32-CAM
  * Used to recognize birds in real-time. sends stream to a server running on a personal machine.
* Arduino-UNO
  * Used to generate bird-scaring sound, and transmit it through speaker.
* Server
  * The "server" is running on a personal computer. Its purpose is to receive the image stream from the ESP32-CAM, decide wether or not is there a bird in frame, and send the output to the Arduino-UNO to continue deterring the bird.

## Project's workflow chart
![workflow_chart](FlowChart.png?raw=true "Workflow chart")

<b>Note:</b> The "model" in question is the AI model we trained to achieve bird recognition.</br>
The model is trained and run using OpenCV and Ultralytics' YOLO in Python.

## Image Streaming

As mentioned before, The image streaming here is done from an AI_THINKER ESP32-CAM module.</br>
This camera is equipped with a Wi-Fi module, which allows us to run a websocket-server on it.</br>
We then run a Python script that receives the image on a different machine (In this case a laptop).

### Running and technical specifications

To run (/activate) the image streaming, enter the Wi-Fi network's credentials into the ```.ino``` file in the correct variables.</br>
Then upload the sketch to the camera, and run the provided Python script on the receiving machine.</br>
<b>Notes:</b></br>
* The receiving machine has to be connected to the same Wi-Fi network as the camera.
* The "stream" is actually an updating image, which will be created in the same folder the script's running in.
* The Python script also prints the timedelta between each two frames.
* To stop the stream, kill the Python script. (This isn't optimal but we need the stream to run indefinitely)
