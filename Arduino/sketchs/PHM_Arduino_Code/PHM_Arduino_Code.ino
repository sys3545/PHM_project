#include <SoftwareSerial.h>

SoftwareSerial BTSerial(8, 9); // 시리얼 통신 객체
int SIG = 7; // 터치 센서 핀번호
int current=0; // 터치 여부
String message=""; // 메세지를 담는 임시 문자열
char out[30]=""; // 최종 보낼 메시지

void setup() {
  // put your setup code here, to run once:
  BTSerial.begin(9600); // 전송 속도 설정
  Serial.begin(9600); // 전송 속도 설정
  pinMode(SIG, INPUT); // SIG 핀을 입력으로 설정
}

void loop() {
  // put your main code here, to run repeatedly:
  current=digitalRead(SIG);

  message=String(current);
  message+=String("\n");
  message.toCharArray(out, message.length()+1);
  BTSerial.write(out);
}
