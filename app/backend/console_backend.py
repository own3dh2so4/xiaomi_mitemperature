from .abstract_backend import AbstractBackend
from .model.measurement import Measurement


class ConsoleBackend(AbstractBackend):
    def send_data(self, measurement: Measurement) -> None:
        print(f"Temperature: {measurement.temperature}")
        print(f"Humidity: {measurement.humidity}")
        print(f"Battery: {measurement.battery}")
        print(f"Timestamp: {measurement.timestamp}")

    def send_error(self, device_name: str) -> None:
        print(f"Error fetching data from '{device_name}'")
