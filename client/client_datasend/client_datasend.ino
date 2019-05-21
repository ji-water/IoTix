#include <ESP8266WiFi.h>
#include <time.h> 
/*const char* ssid = "iptime_ssanta";
const char* password =  "iptimezzaedol";*/
const char* ssid = "SO070VOIPA301"; 
const char* password = "BEED3FA300"; 
/*const uint16_t port = 8080;*/
const uint16_t port = 8090;
/*const char * host = "192.168.200.141";지수*/
/*const char * host = "192.168.0.32";*/
const char * host = "192.168.200.147";

int sensor = A0; //sensor pin
int val; //numeric variable

int loopCount = 0;
boolean flag = true;

WiFiClient client;

/*------------------TIME------------------*/
int timezone = 3; 
int dst = 0; 
 
unsigned long previousMillis = 0;
const long interval = 1000; 

void setup()
{
 
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(sensor, INPUT);

  Serial.setDebugOutput(true); 
   WiFi.mode(WIFI_STA); 
   
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

//TIME
  configTime(9 * 3600, 0,"pool.ntp.org", "time.nist.gov"); 
   Serial.println("\nWaiting for time"); 
   while (!time(nullptr)) { 
     Serial.print("."); 
     delay(1000); 
   }
   Serial.println(""); 
   
}
 
void loop()
{ 
  val = analogRead(sensor);

  //TIME
  unsigned long currentMillis = millis();
  time_t now;
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    if(loopCount==0){
      delay(3000);
      }
    now = time(nullptr); 
  }
 /*-----------------------------------------------*/
 
  if(flag){
    loopCount+=1;
    Serial.println(loopCount);
    if(loopCount == 4){
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
      client.print(ctime(&now));
      client.print(val,DEC); 
    Serial.println(ctime(&now));
    
    
      Serial.println("Disconnecting...");
      client.stop();

      delay(5000);
    }
  }
}
