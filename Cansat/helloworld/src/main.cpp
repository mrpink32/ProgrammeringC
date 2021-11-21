#include <Arduino.h>
#include <string>
#include <WiFi.h>
#include <esp32-hal-ledc.h>

#define LED2 17

void BlinkLED(unsigned char pinNumber, unsigned short int length);

class MorseCodeManager
{
  char charArray[];
public:
  unsigned char pinNumber;
  MorseCodeManager(unsigned char pinNumber);
  void String2Morse(String input)
  {
    for (unsigned char i = 0; i < input.length(); i++)
    {
      Char2Morse(input[i]);
      delay(1000);
    }
  }
  ~MorseCodeManager();
private:
  const unsigned short int longDelay = 500;
  const unsigned short int shortDelay = 250;
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
  void Char2Morse(char data)
  {
    /* todo maybe make some kind of list that contains the
    corresponding amount of blinks to it's char*/
    switch (data)
    {
    case 'a':
      ShortBlink();
      LongBlink();
      break;
    case 'b':
      LongBlink();
      ShortBlink();
      ShortBlink();
      ShortBlink();
    default:
      break;
    }
  }
};

MorseCodeManager::MorseCodeManager(unsigned char pinNumber)
{
  this->pinNumber = pinNumber;
}

MorseCodeManager::~MorseCodeManager()
{
}

const char ssid[] = "CableBox-9027";
const char pass[] = "u2y3ygmmtj";
MorseCodeManager mcm(LED2);

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
  while (true)
  {
    input = Serial.readString();
    if (input.length() > 0)
    {
      break;
    }
  }
  mcm.String2Morse(input);
  //BlinkLED(LED2, 250);
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
