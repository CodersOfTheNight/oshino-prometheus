import aiohttp

from oshino import Agent

from oshino_prometheus.utils import parse_prometheus_metrics


class PrometheusAgent(Agent):

    def endpoints(self):
        return self._data["endpoints"]

    async def get_raw_metrics(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    async def process(self, event_fn):
        logger = self.get_logger()

        for endpoint in endpoints:
            raw = await self.get_raw_metrics(endpoint)
            metrics = parse_prometheus_metrics(raw)

            for key, metric in metrics.items():
                logger.debug("Received metric: {0}".format(metric))
                val, meta = metric
                service = self.prefix + key
                event_fn(metric_f=val,
                         state="ok",
                         service=service,
                         attrs=meta)
