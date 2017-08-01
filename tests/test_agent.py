from pytest import fixture, mark
from prometheus_client import start_http_server, Counter

from oshino_prometheus.agent import PrometheusAgent


@fixture
def prometheus_agent():
    cfg = {"name": "prometheus",
           "endpoints": ["http://localhost:8999"]
           }
    return PrometheusAgent(cfg)


@fixture
def server():
    start_http_server(8999)


@mark.asyncio
async def test_is_reachable(prometheus_agent, server):
    reached = False

    def stub_event_fn(*args, **kwargs):
        nonlocal reached
        reached = True

    await prometheus_agent.process(stub_event_fn)

    assert reached


@mark.asyncio
async def test_is_metrics_output(prometheus_agent, server):
    c = Counter("my_counter", "Counter for testing")
    c.inc(42)

    results = []

    def stub_event_fn(*args, **kwargs):
        nonlocal results
        results.append(kwargs)

    await prometheus_agent.process(stub_event_fn)

    assert len(results) > 0

    tail = results[-1]
    assert tail["service"] == "prometheus.my.counter"
    assert tail["metric_f"] == 42
