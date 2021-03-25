#include <SoftwareSerial.h>

int charging = 8;       // the number of the charging transistor
int thermistor = A3;

int charge = true;    // charge to toggle
int analog_value = analogRead(A5);
int input_voltage = (analog_value * 5.0) / 1024.0;
int starttime = 0;
int vo;
float R1 = 100000;
float logR2, R2, T, Tc;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
int runcode = true;

long timer = 0;
int tcheck = false;

void setup()
{
  pinMode(charging, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT); //LED to check current status

  Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB port only
    }
}

void loop()
{
  if (runcode == true) {
    vo = analogRead(thermistor);
    R2 = R1 * (1023.0 / (float)vo - 0.1);
    logR2 = log(R2);
    T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
    Tc = T - 273.15;
    Tc = Tc * -1.0;
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
        Serial.print(voltage);
        Serial.print(",");
        Serial.println(Tc);
      }
      if (voltage < 1.0) {
        Serial.println(255);
        runcode = false;
      }
    }
  }
}

 
