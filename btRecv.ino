#include <SoftwareSerial.h>
#include "RedMP3.h"

void(* resetFunc) (void) = 0;

#define MP3_RX 4
#define MP3_TX 2

MP3 mp3(MP3_RX, MP3_TX);

int8_t volume = 0x1a;
int8_t folderName = 0x01;
int8_t fileName = 0x01;

int state;
bool flag;

void setup(){
    delay(500); /*Delay neccessary for initialization on mp3 object*/
    mp3.setVolume(volume);
    delay(50); /*Same here*/

    Serial.begin(9600);

    flag = false;
    state = 0;

    if(Serial.available() > 0){
        state = Serial.read(); /*Reads first byte from input buffer*/
    }

    switch(state){
        case '1':
            mp3.playWithFileName(01,001);
            flag = true;
            break;
        case '2':
            mp3.playWithFileName(01,002);
            flag = true;
            break;
        case '3':
            mp3.playWithFileName(01,003);
            flag = true;
            break;
        default:
            break;
    }
    /*If we played a song*/
    if(flag){
        delay(3024);
        Serial.end();
    }
    delay(50);
}

void loop(){
    resetfunc();
}