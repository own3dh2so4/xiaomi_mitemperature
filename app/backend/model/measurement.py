from dataclasses import dataclass


@dataclass
class Measurement:
    name: str
    temperature: float
    humidity: int
    voltage: float
    battery: int
    timestamp: int
