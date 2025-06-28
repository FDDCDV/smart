
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

IOTHUB_CONNECTION_STRING = "HostName=SmartAgriculturar.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=Ajk1CiBxZsxeCW9JXmQnyw7/Tc4lPzJ3GAIoTJuKiJ4="
DEVICE_ID = "plant-device-01"

def send_led_command(status: str):
    manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

    method = CloudToDeviceMethod(
        method_name="ledControl",
        payload=status,
        response_timeout_in_seconds=30
    )

    response = manager.invoke_device_method(DEVICE_ID, method)
    return response.status
