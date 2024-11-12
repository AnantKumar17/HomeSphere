# device-control-service/src/main.py
from fastapi import FastAPI, HTTPException
from models import DeviceCommand
import httpx
import uvicorn

app = FastAPI(title="Device Control Service")

DEVICE_REGISTRY_URL = "http://device-registry-service:8000"

@app.post("/devices/{device_id}/command")
async def send_command(device_id: int, command: DeviceCommand):
    # Check device status
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DEVICE_REGISTRY_URL}/devices/{device_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Device not found")
        
        device = response.json()
        if device["status"] == "offline":
            raise HTTPException(status_code=400, detail="Device is offline")

    # Process command
    command_result = process_command(device_id, command)
    
    # Update device status if needed
    if command_result["status_change"]:
        await client.put(
            f"{DEVICE_REGISTRY_URL}/devices/{device_id}/status",
            params={"status": command_result["new_status"]}
        )

    return command_result

def process_command(device_id: int, command: DeviceCommand):
    # Simulate command processing
    return {
        "device_id": device_id,
        "command": command.command,
        "status": "success",
        "status_change": True,
        "new_status": "active"
    }

# device-control-service/src/models.py
from pydantic import BaseModel

class DeviceCommand(BaseModel):
    command: str
    parameters: dict = {}
