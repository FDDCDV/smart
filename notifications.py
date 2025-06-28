
from blob_utils import read_latest_blob

def get_alerts():
    data = read_latest_blob()
    alerts = []

    if "soilMoisture" in data and data["soilMoisture"] < 40:
        alerts.append("Gleba jest zbyt sucha – podlej roślinę.")
    if "lightLevel" in data and data["lightLevel"] < 200:
        alerts.append("Za mało światła – włączono LED do wspomagania wzrostu.")

    return alerts
