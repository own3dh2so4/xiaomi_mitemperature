from queue import SimpleQueue
from typing import List, Optional

from bluepy import btle  # type: ignore
from bluepy.btle import BTLEDisconnectError

from backend.model.measurement import Measurement
from delegate import Delegate


class MiTemperature:
    def __init__(self, name: str, bluetooth_mac: str) -> None:
        self.name = name
        self.bluetooth_mac = bluetooth_mac
        self.measurements: SimpleQueue[Measurement] = SimpleQueue()
        self.delegate = Delegate(name)
        self.connection: Optional[btle.Peripheral] = None

    def connect(self, conn_retries: int = 1) -> bool:
        retries = 0
        while self.connection is None and retries < conn_retries:
            conn_retries += 1
            try:
                p = btle.Peripheral(self.bluetooth_mac)
                val = b"\x01\x00"
                # enable notifications of Temperature, Humidity and Battery voltage
                p.writeCharacteristic(0x0038, val, True)
                p.writeCharacteristic(0x0046, b"\xf4\x01\x00", True)
                p.withDelegate(self.delegate)
                self.connection = p
            except BTLEDisconnectError:
                print(f"Error connecting with device {self.name}({self.bluetooth_mac})")
        return self.connection is not None

    def disconnect(self) -> None:
        if self.connection:
            self.connection.disconnect()

    def fetch_measurements_from_device(self) -> bool:
        fetched = False
        if self.connection:
            fetched = self.connection.waitForNotifications(2000)
            if fetched:
                measurement = self.delegate.get_last_measurement()
                if measurement:
                    self.measurements.put(measurement)
        return fetched

    def get_measurements(self) -> List[Measurement]:
        measurements = []
        while not self.measurements.empty():
            measurements.append(self.measurements.get())
        return measurements
