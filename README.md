# ESP32_Sensor_GoogleCloud
ESP32 sending sensor's reading (Hall sensor) to Google Cloud IoT via MQTT

The Hall sensor measures magnetic field perpendicular to its location on ESP32 board. Framwork: Arduino. The project is built in PlatformIO.

I'm using [google-cloud-iot-arduino](https://github.com/GoogleCloudPlatform/google-cloud-iot-arduino) and structure it to build in Platform IO. 
`main.py` and `requirements.txt` are only for later visualization using Cloud Function (not for programming ESP32)

I hope anyone find this documentation helpful :smiley:.

## Visualization of data can be achieved with Firebase or InFluxDB integrated with Cloud Function
![image](https://user-images.githubusercontent.com/55075721/140731627-f4d5f54f-49ae-460a-8735-443c0574ecc3.png)

In this case, I let Cloud Function be triggered by pub/sub then call InFluxDB. 
1. Create InFluxDB account 
2. Create a bucket 
3. Generate API Token of that bucket
4. Create a Cloud Function triggered by pub/sub
5. Modify `main.py` in Cloud Function as in my example
6. Include `influxdb-client` in `requirements.txt`

There are many ways to conduct steps 4,5,6. The easiest way is to use Console UI. 

Finally, open InfluxDB, choose your bucket, value field and push `SUBMIT` to see the visualization.
# Note: problems I faced 
## Wifi connection 
If you're using Wifi router with both 2.4GHz and 5GHz, do a wifi scan on ESP32 first to check your exact SSID. Your SSID should not have any space.
## SSL certificate
To get SSL certificate, download the primary and backup certificate from https://cloud.google.com/iot/docs/how-tos/mqtt-bridge#downloading_mqtt_server_certificates (Google's minimal root CA set (<1 KB) for mqtt.2030.ltsapis.goog)
```
openssl x509 -inform DER -in gtsltsr.crt -out primary.pem -text
openssl x509 -inform DER -in GSR4.crt -out secondary.pem -text
```
Run commands to convert the file and copy content from both files to `root_cert` in `ciotc_config.h`. Or you can just copy certificate from my example (include/ciotc_config.h). 

In the google-cloud-iot-arduino library, the certificate is not used to establish connection so you might face problem: `Settings incorrect or missing a cyper for SSL`. 

The fix I used is to change `netClient` class to `WiFiClientSecure` 
- In `esp32-mqtt.h` (line 36)
- In `CloudIoTCoreMqtt.cpp` (line 27) 
- In `CloudIoTMqtt.h` (line 36, 40) 

Then `#include <WiFiClientSecure.h>` in `CloudIoTMqtt.h`. 

In `esp32-mqtt.h`, set certificate
```
void setupCloudIoT()
{
  device = new CloudIoTCoreDevice(
      project_id, location, registry_id, device_id,
      private_key_str);

  setupWifi();
  netClient = new WiFiClientSecure();
  netClient->setCACert(root_cert); //  Set certificate

  mqttClient = new MQTTClient(512);
  mqttClient->setOptions(180, true, 1000); // keepAlive, cleanSession, timeout
  mqtt = new CloudIoTCoreMqtt(mqttClient, netClient, device);
  mqtt->setUseLts(true);
  mqtt->startMQTT();
}
```














