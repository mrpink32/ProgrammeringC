#include <Arduino.h>
#include <string>
#include <WiFi.h>
#include <esp32-hal-ledc.h>

#define LED2 17

void BlinkLED(unsigned char pinNumber, unsigned short int length);

class MorseCodeManager
{
  String input;
  unsigned char pinNumber;
public:
  MorseCodeManager(String input, unsigned char pinNumber);
  ~MorseCodeManager();
private:
  const unsigned char longDelay = 500;
  const unsigned char shortDelay = 250;
  void LongBlink()
  {
    digitalWrite(pinNumber, HIGH);
    delay(longDelay);
    digitalWrite(pinNumber, LOW);
    delay(longDelay);
  }
  void ShortBlink()
  {
    digitalWrite(pinNumber, HIGH);
    delay(shortDelay);
    digitalWrite(pinNumber, LOW);
    delay(shortDelay);
  }
};

MorseCodeManager::MorseCodeManager(String input, unsigned char pinNumber)
{
  this->input = input;
  this->pinNumber = pinNumber;
}

MorseCodeManager::~MorseCodeManager()
{
}





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
  pinMode(LED2, OUTPUT);
}

unsigned short int value = 1;

void loop()
{
  // put your main code here, to run repeatedly:
  String input;
  while (true)//Serial.available()>0
  {
    input = Serial.readString();
    if (input.length() > 0)
    {
      break;
    }
  }
  // todo convert input to morsecode
  BlinkLED(LED2, 250);
  Serial.print("It worked: "+input+"\n");







  //Serial.printf("Dav: %d\n", value);
  // for (int i = 0; i < value; i++)
  // {
  //   BlinkLED(17);
  // }
  // delay(1000);
  // value++;
}

void BlinkLED(unsigned char pinNumber, unsigned short int length)
{
  digitalWrite(pinNumber, HIGH);
  delay(length);
  digitalWrite(pinNumber, LOW);
  delay(length);
}
