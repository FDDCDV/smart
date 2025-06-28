
from blob_utils import read_latest_blob
from sendgrid_notify import send_notification_email

def check_soil_and_notify():
    data = read_latest_blob()
    soil = data.get("soilMoisture")

    if soil is None:
        return {"error": "Brak danych o wilgotności gleby."}

    if soil < 40:
        subject = "Alert: Zbyt niska wilgotność gleby"
        message = f"Wartość wilgotności: {soil}%. Roślina wymaga podlania."
        email_status = send_notification_email(subject, message)
        return {"soilMoisture": soil, "alert": "wysłano e-mail", "email_result": email_status}

    return {"soilMoisture": soil, "alert": "OK"}
