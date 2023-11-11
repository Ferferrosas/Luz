#include <Wire.h>
#include <MAX3010x.h>

MAX30102 sensor1;
MAX30102 sensor2;
MAX30102 sensor3;

int C_sensor1=1;
int C_sensor2=2;
int C_sensor3=3;

int EMG_1 = A0;
int EMG_2 = A1;
int EMG_3 = A2;


float xIR1 = 0;
float yIR1 = 0;
float xIR=0;

float xR1 = 0;
float yR1 = 0;
float xR=0;

float xE1 = 0;
float yE1 = 0;
float xE=0;

float B[] = {0.9967,-0.9967}; // Coeficientes 'b' del filtro
float A[] = {1.0000, -0.9934}; // Coeficientes 'a' del filtro

void TCA9548A(uint8_t bus) {
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          
  Wire.endTransmission();
}

void DataRead(MAX30102 sensor, int bus, int Canal_EMG) {

   TCA9548A(bus); 
    auto sample = sensor.readSample(1000);
  xIR=sample.ir;

   //Calcula la señal filtrada
  float yIR = B[0] * xIR + B[1] * xIR1 - A[1] * yIR1;
  xIR1 = xIR;
  yIR1 = yIR;

  Serial.print(yIR);
  Serial.print(",");
  
  xR=sample.red;

   //Calcula la señal filtrada
  float yR = B[0] * xR + B[1] * xR1 - A[1] * yR1;
  xR1 = xR;
  yR1 = yR;

  Serial.print(yR);
  Serial.print(",");

  xE=analogRead(Canal_EMG);

   //Calcula la señal filtrada
  float yE = B[0] * xE + B[1] * xE1 - A[1] * yE1;
  xE1 = xE;
  yE1 = yE;
  
  Serial.print(xE);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  TCA9548A(C_sensor1);
  sensor1.begin();
  sensor1.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor1.setSamplingRate(5);

  TCA9548A(C_sensor2);
  sensor2.begin();
  sensor2.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor2.setSamplingRate(5);

  TCA9548A(C_sensor3);
  sensor3.begin();
  sensor3.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor3.setSamplingRate(5);
  
}

void loop() {

  
  DataRead(sensor1, C_sensor1, EMG_1);
  Serial.print(",");
  DataRead(sensor2, C_sensor2, EMG_2);
  Serial.print(",");
  DataRead(sensor3, C_sensor3, EMG_3);
  Serial.println();
}
