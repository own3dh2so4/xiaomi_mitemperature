import time
from typing import Optional

from bluepy import btle  # type: ignore

from backend.model.measurement import Measurement


class Delegate(btle.DefaultDelegate):
    def __init__(self, name: str):
        btle.DefaultDelegate.__init__(self)
        self._last_measurement: Optional[Measurement] = None
        self.name = name

    def handleNotification(self, c_handle: int, data: bytes) -> None:
        try:
            timestamp = int(time.time())
            temperature = (
                int.from_bytes(data[0:2], byteorder="little", signed=True) / 100
            )
            humidity = int.from_bytes(data[2:3], byteorder="little")
            voltage = int.from_bytes(data[3:5], byteorder="little") / 1000.0
            battery_level = min(int(round((voltage - 2.1), 2) * 100), 100)
            self._last_measurement = Measurement(
                temperature=temperature,
                humidity=humidity,
                voltage=voltage,
                battery=battery_level,
                timestamp=timestamp,
                name=self.name,
            )
        except Exception as e:
            print("Fail!")
            print(e)

    def get_last_measurement(self) -> Optional[Measurement]:
        measurement = self._last_measurement
        self._last_measurement = None
        return measurement
