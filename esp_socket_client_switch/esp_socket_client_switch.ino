#include <Bounce2.h>
#include <ESP8266WiFi.h>
#define TOUCH_SW 4
#define LED 2

//const char* ssid = "iptime_ssanta";
//const char* password =  "iptimezzaedol";
const char* ssid = "KING_wifi";
const char* password =  "king15963";
//const char * host = "192.168.0.32";
const char * host = "192.168.83.37";
//const uint16_t port = 8090;
const uint16_t port = 8080;

Bounce debouncer = Bounce();
WiFiClient client;

float len = 20; //initial len
char current ='n'; //initial state
unsigned long prev_time=0;
float speed=0;
float section_time=0;

void setup()
{
  Serial.begin(9600);
  pinMode(TOUCH_SW,INPUT);
  pinMode(LED,OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  debouncer.attach(TOUCH_SW);
  debouncer.interval(50);
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
    client.print("stem1");
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
  
void print_info(float speed, float section_time,int len,int len_cnt){
    Serial.print(speed);
    Serial.println("mm/sec");
    Serial.print(section_time);
    Serial.println("sec");
    Serial.println(len);
    Serial.print(len_cnt); //자리수
  }
  
void loop()
{
  unsigned long current_time = millis();
  debouncer.update();
  int value = debouncer.read();
  int len_cnt=0;

  if ( current =='n' && value == LOW ) {
    current = 'y';
    conn_client();
    digitalWrite(LED, HIGH );
    Serial.println("touched");
    section_time=(current_time-prev_time)/1000;//sec
    speed = (1.0/section_time); //mm/sec
    len+=1.0;
    len_cnt = count(len);
    send_server(section_time,speed,len,len_cnt);//section_time sec
    print_info(speed,section_time,len,len_cnt);
    prev_time = current_time;
    Serial.println("Disconnecting...");
    client.stop();
  } 
  else if(current=='y' && value != LOW){
    current = 'n';
    conn_client();
    digitalWrite(LED, LOW );
    Serial.println("untouched");
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


//boolean touchVAL=digitalRead(TOUCH_SW);
//Serial.println(touchVAL);

}
