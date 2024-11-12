# device-control-service/src/models.py
from pydantic import BaseModel

class DeviceCommand(BaseModel):
    command: str
    parameters: dict = {}
