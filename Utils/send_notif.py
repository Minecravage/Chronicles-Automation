import requests
import os

def send_notif(data):
    r = requests.post(str(os.getenv("WEBHOOK_DISCORD")), json=data)
    return r.status_code