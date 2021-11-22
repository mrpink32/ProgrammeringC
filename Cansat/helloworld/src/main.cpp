#include <Arduino.h>
#include <string>
#include <WiFi.h>
#include <esp32-hal-ledc.h>
#include <ctime>

#define LED2 17

void BlinkLED(unsigned char pinNumber, unsigned short int length);

class MorseCodeManager
{
  const int oneUnit = 1000;
  const int threeUnits = 3 * oneUnit;
  const int wordSwitchDelay = 7 * oneUnit;

public:
  unsigned char pinNumber;
  MorseCodeManager(unsigned char pinNumber);
  void GetString4Morse(String input)
  {
    for (unsigned char i = 0; i < input.length(); i++)
    {
      GetChar4Morse(input[i]);
      delay(threeUnits);
    }
  }
  ~MorseCodeManager();

private:
  void LongBlink(unsigned char repeatCount)
  {
    for (unsigned char i = 0; i < repeatCount; i++)
    {
      digitalWrite(pinNumber, HIGH);
      delay(threeUnits);
      digitalWrite(pinNumber, LOW);
      delay(oneUnit);
    }
  }
  void ShortBlink(unsigned char repeatCount)
  {
    for (unsigned char i = 0; i < repeatCount; i++)
    {
      digitalWrite(pinNumber, HIGH);
      delay(oneUnit);
      digitalWrite(pinNumber, LOW);
      delay(oneUnit);
    }
  }
  void GetChar4Morse(char data)
  {
    /* todo maybe make some kind of list that contains the
    corresponding amount of blinks to it's char*/
    switch (data)
    {
    case 'a':
      ShortBlink(1);
      LongBlink(1);
      break;
    case 'b':
      LongBlink(1);
      ShortBlink(3);
      //ShortBlink();
      //ShortBlink();
      break;
    case 'c':
      LongBlink(1);
      ShortBlink(1);
      LongBlink(1);
      ShortBlink(1);
      break;
    case 'd':
      LongBlink(1);
      ShortBlink(2);
      //ShortBlink();
      break;
    case 'e':
      ShortBlink(1);
      break;
    case 'f':
      ShortBlink(2);
      //ShortBlink();
      LongBlink(1);
      ShortBlink(1);
      break;
    case 'g':
      LongBlink(2);
      //LongBlink();
      ShortBlink(1);
      break;
    case 'h':
      ShortBlink(4);
      //ShortBlink();
      //ShortBlink();
      //ShortBlink();
      break;
    case 'i':
      ShortBlink(2);
      //ShortBlink();
      break;
    case 'j':
      ShortBlink(1);
      LongBlink(3);
      //LongBlink();
      //LongBlink();
      break;
    case 'k':
      LongBlink(1);
      ShortBlink(1);
      LongBlink(1);
      break;
    case 'l':
      ShortBlink(1);
      LongBlink(1);
      ShortBlink(2);
      //ShortBlink();
      break;
    case 'm':
      LongBlink(2);
      //LongBlink();
      break;
    case 'n':
      LongBlink(1);
      ShortBlink(1);
      break;
    case 'o':
      LongBlink(3);
      //LongBlink();
      //LongBlink();
      break;
    case 'p':
      ShortBlink(1);
      LongBlink(2);
      //LongBlink();
      ShortBlink(1);
      break;
    case 'q':
      LongBlink(2);
      //LongBlink();
      ShortBlink(1);
      LongBlink(1);
      break;
    case 'r':
      ShortBlink(1);
      LongBlink(1);
      ShortBlink(1);
      break;
    case 's':
      ShortBlink(3);
      //ShortBlink();
      //ShortBlink();
      break;
    case 't':
      LongBlink(1);
      break;
    case 'u':
      ShortBlink(2);
      //ShortBlink();
      LongBlink(1);
      break;
    case 'v':
      ShortBlink(3);
      //ShortBlink();
      //ShortBlink();
      LongBlink(1);
      break;
    case 'w':
      ShortBlink(1);
      LongBlink(2);
      //LongBlink();
      break;
    case 'x':
      LongBlink(1);
      ShortBlink(2);
      //ShortBlink();
      LongBlink(1);
      break;
    case 'y':
      LongBlink(1);
      ShortBlink(1);
      LongBlink(2);
      //LongBlink();
      break;
    case 'z':
      LongBlink(2);
      //LongBlink();
      ShortBlink(2);
      //ShortBlink();
      break;
    case '1':
      ShortBlink(1);
      LongBlink(4);
      break;
    case '2':
      ShortBlink(2);
      LongBlink(3);
      break;
    case '3':
      ShortBlink(3);
      LongBlink(2);
      break;
    case '4':
      ShortBlink(4);
      LongBlink(1);
      break;
    case '5':
      ShortBlink(5);
      break;
    case '6':
      LongBlink(1);
      ShortBlink(4);
      break;
    case '7':
      LongBlink(2);
      ShortBlink(3);
      break;
    case '8':
      LongBlink(3);
      ShortBlink(2);
      break;
    case '9':
      LongBlink(4);
      ShortBlink(1);
      break;
    case '0':
      LongBlink(5);
      break;
    case ' ':
      delay(wordSwitchDelay);
      break;
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
  // while (true)
  // { 
  //   if (WiFi.isConnected())
  //   {
  //     Serial.printf("Connection status: %d\n", WiFi.isConnected());
  //     break;
  //   }
  // }
  pinMode(LED2, OUTPUT);
}

unsigned short int value = 1;

void loop()
{
  // put your main code here, to run repeatedly:
  String input;
  while (true)
  {
    input = Serial.readString(); // maybe use read string until newline
    if (input.length() > 0)
    {
      break;
    }
  }
  mcm.GetString4Morse(input);
  Serial.print("It worked: " + input + "\n");

  //Serial.printf("Dav: %d\n", value);
  // for (int i = 0; i < value; i++)
  // {
  //   BlinkLED(LED2, 250);
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
