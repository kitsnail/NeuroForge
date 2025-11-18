# core/logger.py
import sys
import datetime

def log(*args, **kwargs):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[NeuroForge {ts}]", *args, **kwargs)
    sys.stdout.flush()
