
from fastapi import FastAPI, Body
from led_control import send_led_command
from blob_utils import read_latest_blob
from notifications import get_alerts
from auto_control import auto_led_control
from alerts_email import check_soil_and_notify
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Smart Agricultiral API działa"}

@app.post("/device/led")
def control_led(status: str = Body(..., embed=True)):
    try:
        result = send_led_command(status)
        return {"status": f"Wysłano LED {status}", "result": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/sensor/latest")
def get_latest_data():
    data = read_latest_blob()
    return data

@app.get("/notifications")
def notifications():
    alerts = get_alerts()
    return {"alerts": alerts}

@app.post("/auto-control")
def auto_control():
    result = auto_led_control()
    return result

@app.post("/check-moisture")
def check_moisture():
    result = check_soil_and_notify()
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
