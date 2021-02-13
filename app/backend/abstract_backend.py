from abc import ABC, abstractmethod

from .model.measurement import Measurement


class AbstractBackend(ABC):
    @abstractmethod
    def send_data(self, measurement: Measurement) -> None:
        ...
