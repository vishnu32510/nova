from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()
scheduler.start()
ALARMS = {}

def _fire(alarm_id: str):
    a = ALARMS.get(alarm_id)
    print(f"ALARM: {a}")
    # TODO: notify WebSocket clients via a pubsub or in-memory broker


def set_alarm(time_iso: str, label: str = "Alarm"):
    dt = datetime.fromisoformat(time_iso)
    job = scheduler.add_job(_fire, 'date', run_date=dt, args=[f"job-{dt.timestamp()}"])
    aid = job.id
    ALARMS[aid] = {"id": aid, "time_iso": time_iso, "label": label}
    return ALARMS[aid]

def list_alarms():
    return list(ALARMS.values())

def cancel_alarm(id: str):
    scheduler.remove_job(id)
    return {"id": id, "status": "canceled"}

def alarm_action(action: str, id: str, minutes: int = 5):
    if action == "snooze":
        now = datetime.now(); dt = now + timedelta(minutes=minutes)
        return set_alarm(dt.isoformat(), label=f"Snooze of {id}")
    if action == "dismiss":
        return cancel_alarm(id)
    return {"error": "unknown action"}

