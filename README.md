# ESP32_Sensor_GoogleCloud
ESP32 sending sensor's reading (Hall sensor) to Google Cloud IoT via MQTT

The Hall sensor measures magnetic field perpendicular to its location on ESP32 board. Framwork: Arduino. The project is built in PlatformIO.

The library is based on [google-cloud-iot-arduino] (https://github.com/GoogleCloudPlatform/google-cloud-iot-arduino) and structured to play nicely alongside Platform IO. 

# Note: problems I faced 
## Wifi connection 
If you're using Wifi router with both 2.4GHz and 5GHz, do a wifi scan on ESP32 first to check your exact SSID. Your SSID should not have any space.
## SSL certificate
To get SSL certificate, download the primary and backup certificate from https://cloud.google.com/iot/docs/how-tos/mqtt-bridge#downloading_mqtt_server_certificates. 
```
openssl x509 -inform DER -in gtsltsr.crt -out primary.pem -text
openssl x509 -inform DER -in GSR4.crt -out secondary.pem -text
```
Run commands to convert the file and copy content from both files to `root_cert` in 'ciotc_config.h". Or you can just copy certificate from my example. 

In the google-cloud-iot-arduino library, the certificate is not used to establish connection so you might face problem: `setting missing SSL or wrong configuration`. 

The fix I used is to change `netClient` class to `WiFiClientSecure` in line 36 in esp32-mqtt.h. 

Similar changes should be made in `CloudIoTCoreMqtt.cpp` and `CloudIoTMqtt.h` (line 36, 40, line 27) and `include <WiFiSecureClient.h>` in `CloudIoTMqtt.h`. 

In `ciotc_config.h`, set certificate in `void setupCloudIoT()` by inserting `netClient->setCACert(root_cert)` 
## Visualization of data can be achieved with Firebase or InFluxDB












