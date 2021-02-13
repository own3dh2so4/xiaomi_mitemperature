# Xiaomi Mi temperature

Python app to fetch data form Xiaomi MiTemperature device.

## Usage

```
$ python app --help
Usage: app [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  console
  prometheus
```

```
$ python app console despacho XX:XX:XX:XX:XX:XX 
Metric fetched from device despacho
Temperature: 19.0
Humidity: 69
Battery: 67
Timestamp: 1613213460
Metrics send from device despacho
```

```
python app prometheus --help                     
Usage: app prometheus [OPTIONS] NAME DEVICE

Arguments:
  NAME    Device name  [required]
  DEVICE  Device bluetooth MAC  [required]

Options:
  --url TEXT  Prometheus pushgateway url  [default: pushgateway.home]
  --help      Show this message and exit.
```