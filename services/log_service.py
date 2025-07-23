import csv, os
from datetime import datetime

LOG_DIR = "log"
IN_CSV   = os.path.join(LOG_DIR, "sms_inbox_log.csv")
SE_CSV   = os.path.join(LOG_DIR, "sms_sent_log.csv")

def log_sms_sent(number, text, status=""):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(SE_CSV, "a", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerow([datetime.now().isoformat(), number, text, status])
