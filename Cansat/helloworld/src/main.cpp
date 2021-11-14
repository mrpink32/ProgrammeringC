#include <Arduino.h>


void setup() {
  // put your setup code here, to run
  Serial.begin(115200);
  pinMode(1, OUTPUT);

}

int value = 1;

void loop() {
  // put your main code here, to run repeatedly:
  Serial.printf("Dav: %d\n", value);
  digitalWrite(1, LOW);
  delay(2000);
  digitalWrite(1, HIGH);
  value++;
}