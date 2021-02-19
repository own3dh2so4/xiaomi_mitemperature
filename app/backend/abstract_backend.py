from abc import ABC, abstractmethod

from .model.measurement import Measurement


class AbstractBackend(ABC):
    @abstractmethod
    def send_data(self, measurement: Measurement) -> None:
        ...

    @abstractmethod
    def send_error(self, device_name: str) -> None:
        ...
