#include <SoftwareSerial.h>
#include "RedMP3.h"

#define MP3_RX 4
#define MP3_TX 2

MP3 mp3(MP3_RX, MP3_TX);

int8_t volume = 0x1a;
int8_t folderName = 0x01;
int8_t fileName = 0x01;

int state;

void setup(){
    delay(500); /*Delay neccessary for initialization on mp3 object*/
    mp3.setVolume(volume);
    delay(50); /*Same here*/

    Serial.begin(9600);
}

void loop(){
    if(Serial.available() > 0){
        state = Serial.read(); /*Reads first byte from input buffer*/
    }

    switch(state){
        case '1':
            mp3.playWithFileName(01,001);
            break;
        case '2':
            mp3.playWithFileName(01,002);
            break;
        default:
            break;
    }

    delay(50);
}