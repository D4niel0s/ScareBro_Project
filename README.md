# Final project - ScareBro™

This project is made as a final project for school in Ort ironi D Modi'in. </br>
<b>Project's goals: Identify incoming birds and scare them away using sound - to save them from certain death via wind turbines.</b>

## Project's hardware components

* ESP32-CAM
  * Used to recognize birds in real time. sends stream to a server running on a personal machine.
* Arduino-uno
  * Used to generate bird-scaring sound, and transmit it through speaker.
* Server
  * The "server" is running on a personal computer. It's purpose is to recieve the image stream from the ESP32-CAM, decide wether or not is there a bird in frame, and sending the output to the Arduino uno to continue deterring the bird.

## Project's workflow chart
![workflow_chart](Untitled.png?raw=true "Workflow chart")

<b>Note:</b> The "model" in question is the AI model we trained to achieve bird recognision.</br>
The model is trained and ran using openCV in python.

## Image streaming

As mentioned before, The image streaming here is done from an AI_THINKER ESP32-CAM module.</br>
This camera is equipped with a wi-fi module, which allowes us to run a websocket-server on it.</br>
We then run a python script which recieves the image on a differrent machine. (In this case a laptop)

### Running and technical specifications

To run (/activate) the image streaming, enter the wi-fi network's credentials into the ```.ino``` file in the correct variables.</br>
Then upload the sketch to the camera, and run the provided python script on the recieving machine.</br>
<b>Notes:</b></br>
* The recieving machine has to be connected to the same wi-fi network as the camera.
* The "stream" is actually an updating image, which will be created in the same folder the script's running in.
* The python script also prints the timedelta between each two frames.
* To stop the stream, kill the python script. (This isn't optimal but we need the stream to run indefinitely)
