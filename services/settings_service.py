import json, os

DEFAULTS = {
    "auto_sms_monitor": True,
    "last_port": None,
    "last_baudrate": None
}

def load_settings(path="settings.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return DEFAULTS.copy()

def save_settings(settings, path="settings.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
