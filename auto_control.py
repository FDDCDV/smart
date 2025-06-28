
from blob_utils import read_latest_blob
from led_control import send_led_command

def auto_led_control():
    data = read_latest_blob()
    light_level = data.get("lightLevel")

    if light_level is None:
        return {"error": "Brak danych o poziomie światła."}

    if light_level < 200:
        status = send_led_command("ON")
        return {"led": "ON", "lightLevel": light_level, "result": status}
    else:
        status = send_led_command("OFF")
        return {"led": "OFF", "lightLevel": light_level, "result": status}
