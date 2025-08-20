import json
import os
from datetime import datetime, timedelta
from pytz import timezone


STATE_FILE = "last_alert.json"
TZ = timezone("Europe/Madrid")

# Load the last alert (time)
def load_last_alert_time():
    if not os.path.exists(STATE_FILE):
        return None
    
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
        return datetime.fromisoformat(data["last_alert"])
    

#Save alert time
def save_alert_time():
    current_time = datetime.now(TZ)
    iso_time = current_time.isoformat()

    with open(STATE_FILE, 'w') as f:
        json.dump({"last_alert": iso_time}, f)


#Check for cooldown on alert
def is_cooldown_active(minutes: int):
    latest = load_last_alert_time()
    if not latest:
        return False
    
    now = datetime.now(TZ)
    return now < latest + timedelta(minutes=minutes)


