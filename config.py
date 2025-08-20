# -*- coding: utf-8 -*-
import json, os

_DEFAULT = {
    "guardian": {
        "inactivity_check_sec": 30,
        "heartbeat_sec": 3
    },
    "eabp": {
        "interval_sec": 10,
        "hard_cap": 512
    }
}

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            pass
    return _DEFAULT
