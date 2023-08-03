#include <Wire.h>
#include <MAX3010x.h>

MAX30102 sensor1;
MAX30102 sensor2;
MAX30102 sensor3;

int EMG_0 = A0;
int EMG_1 = A1;
int EMG_2 = A2;


void TCA9548A(uint8_t bus)
{
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

void DataRead(MAX30102 sensor,int bus, int Canal_EMG)
{
   TCA9548A(bus);
   auto sample = sensor.readSample(1000);
   Serial.print(sample.ir);
  Serial.print(",");
  Serial.print(sample.red);  
  Serial.print(",");
  Serial.print(analogRead(Canal_EMG));

}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  

  TCA9548A(4);
  sensor1.begin();
  sensor1.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor1.setSamplingRate(5);
  
  TCA9548A(5);
  sensor2.begin();
  sensor2.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor2.setSamplingRate(5);

  TCA9548A(6);
  sensor3.begin();
  sensor3.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor3.setSamplingRate(5);
  
}

void loop() {

  //Serial.print(millis()/1000);
  //Serial.print("-->");
  //Serial.print(" ");
  DataRead(sensor1, 4, EMG_0);
  Serial.print(",");
  DataRead(sensor2, 5, EMG_1);
  Serial.print(",");
  DataRead(sensor3, 6, EMG_2);
  Serial.println();


  
}
