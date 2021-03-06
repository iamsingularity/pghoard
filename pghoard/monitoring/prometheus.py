"""
Prometheus client (used to create a Prometheus endpoint)

"""


class PrometheusClient:
    def __init__(self, config):
        self._tags = config.get("tags", {})
        self.metrics = {}

    def gauge(self, metric, value, tags=None):
        self._update(metric, value, tags)

    def increase(self, metric, inc_value=1, tags=None):
        self._update(metric, inc_value, tags)

    def timing(self, metric, value, tags=None):
        self._update(metric, value, tags)

    def unexpected_exception(self, ex, where, tags=None):
        pass

    def get_metrics(self):
        data = []
        for metric, value in self.metrics.items():
            line = '{} {}'.format(metric, value)
            data.append(line)
        return data

    def _update(self, metric, value, tags):
        metric = metric.replace(".", "_")
        tags = {**self._tags, **tags}
        tag_list = []
        for k in sorted(tags.keys()):
            tag_list.append("{}=\"{}\"".format(k, tags[k]))
        encoded_tags = "{{{}}}".format(",".join(tag_list))
        formatted_metric = "{}{}".format(metric, encoded_tags)
        self.metrics[formatted_metric] = value
