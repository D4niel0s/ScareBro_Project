// refer to https://shawnhymel.com/1675/arduino-websocket-server-using-an-esp32/
// To make sure WebSocketServer.h is available:
//    Sketch > Include Library > Manage Libraries
//    Search for "WebSockets Sattler' and install the library named "WebSockets by Markus Sattler"
//
// WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
//            Ensure ESP32 Wrover Module or other board with PSRAM is selected
//            Partial images will be transmitted if image exceeds buffer size
//

#include "esp_camera.h"
#include <WiFi.h>
#include <WebSocketsServer.h>

#define CAMRE_MODEL_AI_THINKER // Has PSRAM
#include "camera_pins.h"

const char* ssid     = "********";
const char* password = "********";


// Globals
WebSocketsServer webSocket = WebSocketsServer(80);
 
//Called on every socket event
void onWebSocketEvent(uint8_t num,WStype_t type,uint8_t * payload,size_t length) {

  switch(type) {

    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;

    case WStype_CONNECTED:
      {
        IPAddress ip = webSocket.remoteIP(num);
        Serial.printf("[%u] Connection from ", num);
        Serial.println(ip.toString());
      }
      break;

    // Echo text message back to client
    case WStype_TEXT:
      Serial.printf("[%u] Text: %s\n", num, payload);
      Serial.println((char*)payload);

      if (String((char*)payload) == "capture")
      {
        Serial.println("Capture Command Received - capturing frame");

        camera_fb_t * fb = NULL;
        //Get and return frame buffer - a workaround to get the latest frame to send
        fb = esp_camera_fb_get();
        esp_camera_fb_return(fb);
        
        fb = NULL;
        fb = esp_camera_fb_get(); // get latest image
        size_t fbsize = fb->len;
        Serial.println(fbsize);
        Serial.println("Image captured. Returning frame buffer data.");
        webSocket.sendBIN(num, fb->buf, fbsize);
        esp_camera_fb_return(fb);
        Serial.println("Done");
      } else
      {
        webSocket.sendTXT(num, payload);
      }
      break;

    // For everything else: do nothing
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
    default:
      break;
  }
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println("Connecting...");

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.grab_mode = CAMERA_GRAB_LATEST; //CAMERA_GRAB_WHEN_EMPTY; //
  
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  }else{
    config.frame_size = FRAMESIZE_QVGA; //FRAMESIZE_96X96; //FRAMESIZE_QQVGA; //FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Msg: Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_UXGA);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  Serial.print("Msg: Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");

  // Start WebSocket server and assign callback
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
}

void loop() {
  // Look for and handle WebSocket data
  webSocket.loop();
}