import datetime
import os

# --- FIX PYTHON PATH SO AUDIT LOG FILE CAN BE ACCESSIBLE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logfile = os.path.join(BASE_DIR, "audit.log")
# ---------------------------------------

# Function to log event related to user activity in our audit log file
def log_event(event, username, details):
    event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{event_time}] {event} | user={username} | {details}\n" 
    with open(logfile, 'a') as f:
        f.write(line)
