import base64
from datetime import datetime
from influxdb_client import InfluxDBClient,Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import jason

def iotcore_pubsub_to_influxdb(event, context):
	"""Triggered from a message on a Cloud Pub/Sub topic.
	Args:
		 event (dict): Event payload.
		 context (google.cloud.functions.Context): Metadata for the event.
	"""
	kind='hallsensor'
  	host = 'host1'
  	device= 'esp32-1'
  	token = "w8lvjmIYvvmTwg7GLMnj6308QlJI4L6G7OcxjfnJl7au1F_wT5bAxFp-Y_RmO10cRJbK4KYc3hxHLvG9nDvJyA=="
  	org = "duongnghiephuy123@gmail.com"
  	bucket = "iotcore Bucket"
  

	client=InfluxDBClient(url="https://europe-west1-1.gcp.cloud2.influxdata.com", token=token, org=org)

  	pubsub_message = base64.b64decode(event['data']).decode('utf-8')
  	iot_data = json.loads(pubsub_message)
  	time_str = datetime.utcfromtimestamp(iot_data['timestamp']).strftime('%Y-%m-%dT%H:%M:%SZ')
  	_send_sensor_data_to_influxdb(client,kind,host,device,iot_data["hall_sensor"],time_str,bucket,org)
  	print("Success");

def _send_sensor_data_to_influxdb(client,kind,host,device,value,time_str,bucket,org):
  	point = Point(kind).tag('host', host).tag('device', device).field('value', value).time(time_str)
  	write_api = client.write_api(write_options=SYNCHRONOUS)
  	write_api.write(bucket=bucket, org=org, record=point)