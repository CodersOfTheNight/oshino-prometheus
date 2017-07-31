import time

import requests

from pytest import fixture
from prometheus_client import start_http_server, Counter

from oshino_prometheus.util import parse_prometheus_metrics


TEST_COUNTER = Counter("my_test_counter", "Used to test counter")


@fixture
def prometheus_service():
    start_http_server(8999)


def test_basic_counter(prometheus_service):
    TEST_COUNTER.inc()
    time.sleep(0.1)
    resp = requests.get("http://localhost:8999")
    assert resp.status_code == 200
    metrics = dict(parse_prometheus_metrics(resp.text))
    assert len(metrics) > 0
    metric = metrics["my_test_counter"]
    val, meta = metric
    assert val == 1
