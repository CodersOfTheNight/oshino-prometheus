oshino-prometheus
=====================
Reads metrics from Prometheus

For more info, refer to parent project [Oshino](https://github.com/CodersOfTheNight/oshino)

Installing
------------
`pip install oshino-prometheus`

Config
-------
* `endpoints` - array of endpoints to collect metrics from, eg. `http://localhost:8000`

Example Config
---------------
```yaml
---
interval: 10
loglevel: DEBUG
riemann:
  host: localhost
  port: 5555
agents:
  - name: prometheus
    module: oshino_prometheus.agent.PrometheusAgent
    tag: prometheus
    endpoints:
      - "http://localhost:8000"
```
