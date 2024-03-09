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
