from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter  # type: ignore

from .abstract_backend import AbstractBackend
from .model.measurement import Measurement


class PrometheusBackend(AbstractBackend):
    def __init__(self, prometheus_url: str = "pushgateway.home"):
        self.prometheus_url = prometheus_url
        self.registry = CollectorRegistry()
        self.t = Gauge(
            "temp_celsius",
            "Temperature, celsius",
            registry=self.registry,
            labelnames=("sensor",),
        )
        self.h = Gauge(
            "humidity_pct",
            "Humidity, percentage",
            registry=self.registry,
            labelnames=("sensor",),
        )
        self.bv = Gauge(
            "battery_pct",
            "Battery, percentage",
            registry=self.registry,
            labelnames=("sensor",),
        )
        self.error = Counter(
            "xiaomi_sensor_fetch_error",
            "Fetch error counter counter",
            registry=self.registry,
            labelnames=("sensor",),
        )

    def send_data(self, measurement: Measurement) -> None:
        self.t.labels(measurement.name).set(measurement.temperature)
        self.h.labels(measurement.name).set(measurement.humidity)
        self.bv.labels(measurement.name).set(measurement.battery)
        push_to_gateway(
            self.prometheus_url,
            job="home_temperature",
            grouping_key={"sensor": measurement.name},
            registry=self.registry,
        )

    def send_error(self, device_name: str) -> None:
        self.error.inc()
        push_to_gateway(
            self.prometheus_url,
            job="home_temperature",
            grouping_key={"sensor": device_name},
            registry=self.registry,
        )
