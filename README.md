## ESP32_Sensor_GoogleCloud
ESP32 sending sensor's reading (Hall sensor) to Google Cloud IoT via MQTT

The Hall sensor measures magnetic field perpendicular to its location on ESP32 board. Framwork: Arduino. The project is built in PlatformIO.

The library is based on [google-cloud-iot-arduino] (https://github.com/GoogleCloudPlatform/google-cloud-iot-arduino) and structured to play nicely alongside Platform IO. 

## Note: problems I faced 
# Wifi connection 
If you're using Wifi router with both 2.4GHz and 5GHz, do a wifi scan on ESP32 first to check your exact SSID. Your SSID should not have any space.
# SSL certificate
To get SSL certificate, download the primary and backup certificate from https://cloud.google.com/iot/docs/how-tos/mqtt-bridge#downloading_mqtt_server_certificates. 


In the original library, the certificate is not used to establish connection so you might face problem: setting missing SSL or wrong configuration. 

The fix is to change 'netClient' class to 'WiFiClientSecure' in line 36 in esp32-mqtt.h. 

Similar changes should be made in CloudIoTCoreMqtt.cpp and CloudIoTMqtt.h 










