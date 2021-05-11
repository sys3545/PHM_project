#include <SoftwareSerial.h>
#include <DHT.h>

SoftwareSerial BTSerial(8, 9); // 시리얼 통신 객체
String message=""; // 메세지를 담는 임시 문자열
char out[30]=""; // 최종 보낼 메시지
// 전압관련
float vout = 0.0; 
float vin = 0.0;
float R1 = 30000.0;
float R2 = 7500.0;
int value = 0;
//
DHT dht(A3,DHT11);
int INA=12;
int INB=13;

void setup() {
  // put your setup code here, to run once:
  BTSerial.begin(9600); // 전송 속도 설정
  Serial.begin(9600); // 전송 속도 설정
  pinMode(A0,INPUT); // 전류센서 인풋 핀
  pinMode(A1,INPUT); // 소리센서 인풋 핀
  pinMode(A2, INPUT); // 전압센서 인풋 핀

  pinMode(INA,OUTPUT);
  pinMode(INB,OUTPUT);
  digitalWrite(INA,HIGH);
  digitalWrite(INB,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  int t = dht.readTemperature();
  int sound = analogRead(A1);
  if(sound > 1000){
    sound-=950;
  }
  int vibe = 1023-analogRead(A3);
  int v = analogRead(A0)-103;
  value = analogRead(A2);
  vout = (value * 5.0) / 1024.0;  //전압값을 계산해주는 공식
  vin = vout / ( R2 / ( R1 + R2) );
  int voltage = (int)(vin*100);
  BTSerial.print('M');
  BTSerial.print(sound);
  BTSerial.print(',');
  BTSerial.print(t);
  BTSerial.print(',');
  BTSerial.print(v);
  BTSerial.print(',');
  BTSerial.print(voltage);
  BTSerial.println();
  
  delay(100);
}
