
import time
import random
import datetime
import json
import sys
import os
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from azure.storage.blob import BlobServiceClient

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from alerts_email import check_soil_and_notify

IOTHUB_CONNECTION_STRING = "HostName=SmartAgriculturar.azure-devices.net;DeviceId=plant-device-01;SharedAccessKey=/WB2vdkgC2FAA/UGKUL0HixbMajhFSs6Qxt4zZTdNvk="
BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=smaqtagriculturar;AccountKey=YAppJcehi/7XM/duo1o5YRSudQH15kFNH4ojTsKD3J5FXFmLrmuVJ+gSHO99lq9USzA4594FdL+a+ASteYxtpw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "sensordata"

device_client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_CONNECTION_STRING)

blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def generate_sensor_data():
    soil_moisture = random.randint(20, 80)
    light_level = random.randint(50, 800)
    return {
        "soilMoisture": soil_moisture,
        "lightLevel": light_level,
        "timestamp": str(datetime.datetime.utcnow())
    }

def write_to_blob(data):
    blob_name = f"reading_{datetime.datetime.utcnow().isoformat()}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(data), overwrite=True)

def method_request_handler(method_request):
    if method_request.name == "ledControl":
        print(f"Odebrano komendę: {method_request.payload}")
        status = 200
        payload = f"LED {method_request.payload} ustawione"
        response = MethodResponse.create_from_method_request(method_request, status, payload)
        device_client.send_method_response(response)

print("Łączenie z Azure IoT Hub...")
device_client.connect()
device_client.on_method_request_received = method_request_handler
print("Połączono. Rozpoczynanie symulacji...")

try:
    while True:
        data = generate_sensor_data()
        message = Message(str(data))
        device_client.send_message(message)
        write_to_blob(data)
        print(f"Wysłano i zapisano dane: {data}")

        email_result = check_soil_and_notify()
        print(f"Alert e-mail: {email_result}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Symulacja przerwana przez użytkownika.")

finally:
    device_client.disconnect()
