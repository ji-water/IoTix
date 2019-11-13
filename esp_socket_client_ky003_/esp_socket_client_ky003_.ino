#include <ESP8266WiFi.h>
#define LED 2

//const char* ssid = "iptime_ssanta";
//const char* password =  "iptimezzaedol";
const char* ssid = "KING_wifi";
const char* password =  "king15963";
//const char * host = "192.168.0.32";
const char * host = "192.168.83.37";
//const uint16_t port = 8090;
const uint16_t port = 8080;

WiFiClient client;

float len = 19; //initial len
char current ='W'; //initial state
unsigned long prev_time=0;
float speed=0;
float section_time=0;
int val;
int sensor = A0;

void setup()
{
  Serial.begin(9600);
  pinMode(sensor,INPUT);
  pinMode(LED,OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}
 
int count(float len){
  int len_cnt = 0;
  int tp = len;
  while(tp>0){
    tp=tp/10;
    len_cnt++;
  }
  return len_cnt;  
}


void send_server(float time,float speed,int len,int len_cnt){
  if(client.connected()){
    client.print("tomato1");
    client.print("stem2");
    client.print(len_cnt,DEC);
    client.print(len,DEC); //누적길이
    client.print(speed,DEC);
    //Serial.println("Disconnecting...");
    //client.stop();
  }
}

void conn_client(){
  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  } 
  Serial.println("Connected to server successful!");  
  }

void conn_client2(){
  while(!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(1000);
  } 
  Serial.println("Connected to server successful!");  
  }  
  
void print_info(float speed, float section_time,int len,int len_cnt){
    Serial.print(speed);
    Serial.println("mm/sec");
    Serial.print(section_time);
    Serial.println("sec");
    Serial.println(len);
    Serial.println(len_cnt); //자리수
  }
  
void loop()
{
  unsigned long current_time = millis();
  int len_cnt=0;
  val = analogRead(sensor);

  if(current =='W'&&val>500) {
    current = 'B';
    conn_client2();
    digitalWrite(LED, HIGH );
    Serial.println("black");
    section_time=(current_time-prev_time)/1000;//sec
    speed = (3.0/section_time); //mm/sec
    len+=3.0;
    len_cnt = count(len);
    send_server(section_time,speed,len,len_cnt);//section_time sec
    print_info(speed,section_time,len,len_cnt);
    prev_time = current_time;
    Serial.println("Disconnecting...");
    client.stop();
  } 
  else if(current =='B'&&val<50){
    current = 'W';
    conn_client2();
    digitalWrite(LED, LOW );
    Serial.println("white");
    section_time=(current_time-prev_time)/1000;
    speed = (2.0/section_time); //mm/sec
    len+=2.0;
    len_cnt = count(len);
    send_server(section_time,speed,len,len_cnt);//section_time sec
    print_info(speed,section_time,len,len_cnt);
    prev_time = current_time;
    Serial.println("Disconnecting...");
    client.stop();
  }


}
