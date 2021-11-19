#include <Arduino.h>
#include <string>
#include <WiFi.h>
#include <esp32-hal-ledc.h>

void BlinkLED(unsigned char pinNumber);

char ssid[] = "CableBox-9027";
char pass[] = "u2y3ygmmtj";

void setup()
{
  // put your setup code here, to run
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (true)
  {
    if (WiFi.isConnected())
    {
      Serial.printf("Connection status: %d\n", WiFi.isConnected());
      break;
    }
  }
  pinMode(17, OUTPUT);
}

unsigned short int value = 1;
String input;
bool inputIsAssigned = false;

void loop()
{
  // put your main code here, to run repeatedly:
  Serial.printf("Dav: %d\n", value);
  while (!inputIsAssigned)
  {
    input = Serial.read();//Serial.readStringUntil('\n');
    if (input.length() < 0)
    {
      break;
    }
  }
  Serial.print(input);
  for (int i = 0; i < value; i++)
  {
    BlinkLED(17);
  }
  delay(1000);
  value++;
}

void BlinkLED(unsigned char pinNumber)
{
  digitalWrite(pinNumber, HIGH);
  delay(250);
  digitalWrite(pinNumber, LOW);
  delay(250);
}
