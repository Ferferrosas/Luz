#include <Wire.h>
#include <MAX3010x.h>

MAX30102 sensor1;
MAX30102 sensor2;
MAX30102 sensor3;

int EMG_0 = A0;
int EMG_1 = A1;
int EMG_2 = A2;

int REF_BAJA_EMG = 100;
int REF_ALTA_EMG = 1000;

void TCA9548A(uint8_t bus)
{
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

void READ_EMG()
{
  Serial.print(REF_BAJA_EMG);
    Serial.print(",");

  
  Serial.print(analogRead(EMG_0));
  Serial.print(",");
  Serial.print(analogRead(EMG_1));
    Serial.print(",");

  Serial.print(analogRead(EMG_2));
    Serial.print(",");

  
  Serial.print(REF_ALTA_EMG);
  delay(5);
}


void READ_RED()
{

   TCA9548A(4);
   auto sample = sensor1.readSample(1000);
   Serial.print(sample.ir);
     Serial.print(",");

   TCA9548A(5);
   sample = sensor2.readSample(1000);
   Serial.print(sample.ir);
     Serial.print(",");

   TCA9548A(6);
   sample = sensor3.readSample(1000);
   Serial.print(sample.ir);

}


void READ_NEAR()
{

   TCA9548A(4);
   auto sample = sensor1.readSample(1000);
   Serial.print(sample.ir);
     Serial.print(",");

   TCA9548A(5);
   sample = sensor2.readSample(1000);
   Serial.print(sample.ir);
     Serial.print(",");

   TCA9548A(6);
   sample = sensor3.readSample(1000);
   Serial.print(sample.ir);

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

  Serial.print(millis()/1000);
  Serial.print("-->");
  Serial.print(" ");
  
  //READ_EMG();
  READ_RED();
  //READ_NEAR();
  Serial.println();


  
}
