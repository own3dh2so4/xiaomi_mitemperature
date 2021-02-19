import re

import typer

from backend import ConsoleBackend
from backend.abstract_backend import AbstractBackend
from backend.prometheus_backend import PrometheusBackend
from mi_temperature import MiTemperature

_BACKEND_PARSER = {
    "console": ConsoleBackend,
    "prometheus": PrometheusBackend,
}
app = typer.Typer()


def _is_valid_bluetooth_mac(bluetooth_mac: str) -> bool:
    return (
        re.search(
            "[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$", bluetooth_mac
        )
        is not None
    )


def _validate_bluetooth_mac(bluetooth_mac: str) -> None:
    if not _is_valid_bluetooth_mac(bluetooth_mac):
        typer.echo(f"Invalid bluetooth MAC '{bluetooth_mac}'", err=True)
        raise typer.Exit(code=1)


def _send_measurement(
    device_name: str, bluetooth_mac: str, backend: AbstractBackend, conn_retries: int = 1
) -> None:
    _validate_bluetooth_mac(bluetooth_mac)
    mi_temperature = MiTemperature(device_name, bluetooth_mac)
    if mi_temperature.connect(conn_retries):
        mi_temperature.fetch_measurements_from_device()
        typer.echo(f"Metric fetched from device {device_name}")
        backend.send_data(mi_temperature.get_measurements()[0])
        typer.echo(f"Metrics send from device {device_name}")
        mi_temperature.disconnect()
    else:
        backend.send_error(device_name)



@app.command()
def console(
    name: str = typer.Argument(..., help="Device name"),
    device: str = typer.Argument(..., help="Device bluetooth MAC"),
) -> None:
    _send_measurement(name, device, ConsoleBackend())


@app.command()
def prometheus(
    name: str = typer.Argument(..., help="Device name"),
    device: str = typer.Argument(..., help="Device bluetooth MAC"),
    url: str = typer.Option("pushgateway.home", help="Prometheus pushgateway url"),
    conn_retries: int = typer.Option(5, help="Bluetooth connection retries")
) -> None:
    _send_measurement(name, device, PrometheusBackend(prometheus_url=url))


if __name__ == "__main__":
    app()
