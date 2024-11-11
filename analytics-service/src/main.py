from fastapi import FastAPI
from models import DeviceEvent
from datetime import datetime, timedelta
import uvicorn

app = FastAPI(title="Analytics Service")

# In-memory storage for demonstration
events = []

@app.post("/events/")
async def record_event(event: DeviceEvent):
    events.append(event)
    return {"message": "Event recorded successfully"}

@app.get("/analytics/device/{device_id}")
async def get_device_analytics(device_id: int, days: int = 7):
    cutoff_date = datetime.now() - timedelta(days=days)
    device_events = [
        event for event in events
        if event.device_id == device_id and event.timestamp >= cutoff_date
    ]
    
    return {
        "device_id": device_id,
        "total_events": len(device_events),
        "event_types": count_event_types(device_events),
        "daily_activity": calculate_daily_activity(device_events)
    }

def count_event_types(device_events):
    event_counts = {}
    for event in device_events:
        event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
    return event_counts

def calculate_daily_activity(device_events):
    daily_activity = {}
    for event in device_events:
        date = event.timestamp.date()
        daily_activity[str(date)] = daily_activity.get(str(date), 0) + 1
    return daily_activity