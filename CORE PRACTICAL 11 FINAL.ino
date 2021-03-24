#include <SoftwareSerial.h>

int charging = 8;       // the number of the charging transistor

int charge = true;    // charge to toggle
int analog_value = analogRead(A5);
int input_voltage = (analog_value * 5.0) / 1024.0;
int starttime = 0;
//int pointcount = 0;

long timer = 0;
int tcheck = false;

void setup()
{
  pinMode(charging, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT); //LED to check current status
  pinMode(A5, INPUT);

  Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB port only
    }
}

void loop()
{
  int sensorValuen = analogRead(A1);
  float voltagen = sensorValuen * (5.0 / 1023.0);
  int sensorValuep = analogRead(A0);
  float voltagep = sensorValuep * (5.0 / 1023.0);
  float voltage = voltagep - voltagen;
  
      if (charge == true){ // toggles charging to have a high voltage (5V), activating the bridge on the transistor
        digitalWrite(charging, HIGH);
        digitalWrite(LED_BUILTIN, HIGH); //LED comes on to tell us it is charging
        if (voltage > 4.01) {
          charge = false;
          tcheck = true;
        }
      } else {  //toggles charging to have a low voltage (<1V), turning off the status LED as well.
        digitalWrite(charging, LOW);
        digitalWrite(LED_BUILTIN, LOW);
        //tcheck = true; 
      }
    
  if (charge == false) {
    if (voltage < 4.01 && voltage > 1.0) {
      if (tcheck == true) {
        starttime = millis();
        tcheck = false;
      }
      timer = millis() - starttime;
      Serial.print(timer);
      Serial.print(",");
      Serial.println(voltage);
      //pointcount += 1;
    }
    if (voltage < 1.0) {
      Serial.println(255);
      //Serial.println(pointcount);
      charge = true;
    }
  }
}

 