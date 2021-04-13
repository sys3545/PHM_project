#include <SoftwareSerial.h>
#include <DHT.h>
#define DHTPIN A1
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial BTSerial(8, 9); // 시리얼 통신 객체
String message=""; // 메세지를 담는 임시 문자열
char out[30]=""; // 최종 보낼 메시지

void setup() {
  // put your setup code here, to run once:
  BTSerial.begin(9600); // 전송 속도 설정
  Serial.begin(9600); // 전송 속도 설정
}

void loop() {
  // put your main code here, to run repeatedly:
<<<<<<< HEAD
  int h = dht.readHumidity();
  int t = dht.readTemperature();

  BTSerial.print('M');
  BTSerial.print(h);
  BTSerial.print(',');
  BTSerial.print(t);
  BTSerial.println();
  delay(100);
=======
  current=digitalRead(SIG);
  
  BTSerial.print(current);
  BTSerial.println();
>>>>>>> 5319b1e59d6350d22585b8705c2169deba5867cf
}
