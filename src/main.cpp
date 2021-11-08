#include <esp32-mqtt.h>

#define PUBLISH_DELAY 60000

unsigned long lastMillis = 0;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  setupCloudIoT();
}

void loop()
{
  float sum = 0;
  float hall_measurement;
  int n = 20;
  // put your main code here, to run repeatedly:
  mqtt->loop();
  delay(10);

  if (!mqttClient->connected())
  {

    connect();
    Serial.println("Connected");
  }

  if (millis() - lastMillis > PUBLISH_DELAY)
  {
    lastMillis = millis();
    for (int i = 0; i < n; i++)
    {
      sum += hallRead();
      delay(10);
    }
    hall_measurement = sum / n;
    String payload = String("{\"timestamp\":") + time(nullptr) +
                     String(",\"hall sensor reading\":") + hall_measurement +
                     String("}");
    ;
    Serial.println(payload);
    publishTelemetry(payload);
  }
}