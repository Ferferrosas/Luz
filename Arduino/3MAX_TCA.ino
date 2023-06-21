#include <Wire.h>
#include <MAX3010x.h>

MAX30102 sensor1;
MAX30102 sensor2;
MAX30102 sensor3;

void TCA9548A(uint8_t bus)
{
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

void DataRead(MAX30102 sensor,int bus)
{
   TCA9548A(bus);
   auto sample = sensor.readSample(1000);
  Serial.print(sample.ir);
  //Serial.print(",");
  //Serial.println(sample.red);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  sensor1.begin();
  sensor2.begin();
  sensor3.begin();
  
  TCA9548A(4);
  if (!sensor1.begin()) {
    Serial.println("Sensor not found, bus 4");
    while (1);
  }
   TCA9548A(5);
  if (!sensor2.begin()) {
    Serial.println("Sensor not found, bus 5");
    while (1);
  }
  TCA9548A(6);
  if (!sensor3.begin()) {
    Serial.println("Sensor not found, bus 6");
    while (1);
  }
int contador=0;
}

void loop() {
  Serial.print(millis()/1000);
  Serial.print("-->");
  Serial.print(" ");
  DataRead(sensor1, 4);
  Serial.print(",");
  DataRead(sensor2, 5);
  Serial.print(",");
  DataRead(sensor3, 6);
  Serial.println();
  delay(1);
}
