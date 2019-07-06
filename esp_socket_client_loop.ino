#include <ESP8266WiFi.h>
/*const char* ssid = "iptime_ssanta";
const char* password =  "iptimezzaedol";*/
/*const char* ssid = "EWHA-IOT";
const char* password = "dscho007";*/
const char* ssid = "KING_wifi";
const char* password = "king15963";
const uint16_t port = 8080;
/*const uint16_t port = 8090;*/
/*const char * host = "192.168.200.141";지수*/
/*const char * host = "192.168.0.32"; 집
/*const char * host = "192.168.0.15";*/
const char * host = "192.168.83.10";
int sensor = A0; //sensor pin
int val; //numeric variable

int loopCount = 0;
boolean flag = true;

float len = 10.0; //초기 길이
char current = 'W';//white
float speed=0;
unsigned long prev_time=0;

WiFiClient client;
void setup()
{
 len = 10.0;
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(sensor, INPUT);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

}
 
void loop()
{ 
  unsigned long current_time = millis();
  val = analogRead(sensor);
  if(current =='W'&&val>500) {
    //검정색 감지
    len+=0.4;
    current ='B';
  }
  else if(current =='B'&&val<50){
    len+=0.2;
    current = 'W';
    }
  if(flag){
    loopCount+=1;
    Serial.println(loopCount);
    Serial.println(len);
    speed = ((len-10)/current_time)*1000;
    Serial.print(speed);
    Serial.println("cm/sec");
    if(loopCount == 10){
      Serial.println("연결종료");
      flag = false;
      return;
   }
    if(!client.connect(host, port)) {
        Serial.println("Connection to host failed");
        delay(1000);
        return;
    }
 
    Serial.println("Connected to server successful!");
 
    if (client.connected()) {
      Serial.print("sensor val:");
      Serial.println(val,DEC);
      client.print("tomato1");
      client.print(len,DEC);
      client.print(speed,DEC); 
    
    
      Serial.println("Disconnecting...");
      client.stop();

      delay(5000);
    }
  }
}
