#include <MAX3010x.h>

MAX30102 sensor;

void setup() {
  Serial.begin(115200);

  // Sensor setup
  sensor.begin();

  // Setup resolution and sampling rate
  sensor.setResolution(MAX30102::RESOLUTION_16BIT_118US);
  sensor.setSamplingRate(5);
}

void loop() {
  auto sample = sensor.readSample(1000);
  Serial.print(sample.ir);
  Serial.print(",");
  Serial.println(sample.red);
}
