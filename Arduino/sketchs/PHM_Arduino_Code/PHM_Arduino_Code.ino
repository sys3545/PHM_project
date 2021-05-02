#include <SoftwareSerial.h>
#include <DHT.h>

#define DHTPIN A1
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial BTSerial(8, 9); // 시리얼 통신 객체
String message=""; // 메세지를 담는 임시 문자열
char out[30]=""; // 최종 보낼 메시지
int angle=0;

void setup() {
  // put your setup code here, to run once:
  BTSerial.begin(9600); // 전송 속도 설정
  Serial.begin(9600); // 전송 속도 설정
  pinMode(A0,INPUT); // 전류센서 인풋 핀
}

void loop() {
  // put your main code here, to run repeatedly:
  int h = dht.readHumidity();
  int t = dht.readTemperature();
  int v = analogRead(A0)-103;
  BTSerial.print('M');
  BTSerial.print(h);
  BTSerial.print(',');
  BTSerial.print(t);
  BTSerial.print(',');
  BTSerial.print(v);
  BTSerial.print(',');
  BTSerial.print(100);
  BTSerial.println();
  
  delay(100);
}
