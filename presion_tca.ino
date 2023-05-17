#include <Wire.h>
#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp180_sensor1;
Adafruit_BMP085 bmp180_sensor2;
Adafruit_BMP085 bmp180_sensor3;

void TCA9548A(uint8_t bus)
{
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

void DataRead(Adafruit_BMP085 sensor,int bus)
{
   TCA9548A(bus);
   float pressure = sensor.readPressure() / 100.0F;
   //Serial.print("Presión: ");
  Serial.print(pressure);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  bmp180_sensor1.begin();
  bmp180_sensor2.begin();
  bmp180_sensor3.begin();
  
  TCA9548A(4);
  if (!bmp180_sensor1.begin()) {
    Serial.println("Could not find a valid MAX30102 sensor on bus 4, check wiring!");
    while (1);
  }
  TCA9548A(5);
  if (!bmp180_sensor2.begin()) {
    Serial.println("Could not find a valid MAX30102 sensor on bus 4, check wiring!");
    while (1);
  }
  TCA9548A(6);
  if (!bmp180_sensor2.begin()) {
    Serial.println("Could not find a valid MAX30102 sensor on bus 4, check wiring!");
    while (1);
  }

}

void loop() {
  Serial.print(millis()/1000);
  Serial.print("-->");
  DataRead(bmp180_sensor1, 4);
  Serial.print(" ");
  DataRead(bmp180_sensor1, 5);
  Serial.print(" ");
  DataRead(bmp180_sensor2, 6);
  Serial.println();
  delay(1);
}
