import time
import random

import requests

from pytest import fixture
from prometheus_client import start_http_server, Counter, Summary

from oshino_prometheus.util import parse_prometheus_metrics


@fixture
def prometheus_service():
    start_http_server(8999)


def test_basic_counter(prometheus_service):
    TEST_COUNTER = Counter("test_basic_counter", "Used to test counter")
    TEST_COUNTER.inc()
    time.sleep(0.1)
    resp = requests.get("http://localhost:8999")
    assert resp.status_code == 200
    metrics = dict(parse_prometheus_metrics(resp.text))
    assert len(metrics) > 0
    metric = metrics["test_basic_counter"]
    val, meta = metric
    assert val == 1


def test_basic_counter_w_labels(prometheus_service):
    TEST_COUNTER = Counter("test_basic_counter_w_labels", "Used to test counter", ["name"])
    TEST_COUNTER.labels(name="test").inc()
    time.sleep(0.1)
    resp = requests.get("http://localhost:8999")
    assert resp.status_code == 200
    metrics = dict(parse_prometheus_metrics(resp.text))
    assert len(metrics) > 0
    metric = metrics["test_basic_counter_w_labels"]
    val, meta = metric
    assert val == 1
    assert meta["name"] == "test"


def test_summary(prometheus_service):
    TEST_SUMMARY = Summary("test_summary", "Used to test summary")

    @TEST_SUMMARY.time()
    def timer_req(t):
        time.sleep(t)

    for i in range(0, 10):
        timer_req(random.randint(0, 10) / 10)

    resp = requests.get("http://localhost:8999")
    assert resp.status_code == 200
    metrics = dict(parse_prometheus_metrics(resp.text))
    assert len(metrics) > 0

    metric_count = metrics["test_summary_count"]
    metric_sum = metrics["test_summary_sum"]
    assert metric_count[0] == 10
    assert metric_sum[0] > 0
