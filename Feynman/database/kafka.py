import json
from collections import defaultdict

from kafka import KafkaProducer, KafkaConsumer

from Feynman.etc.util import get_logger


class Kafka_queue_consumer():
    def __init__(self, opt):
        self._opt = opt
        self._kc = KafkaConsumer(self._opt.topic,
                                 bootstrap_servers=self._opt.bootstrap_servers,
                                 group_id=self._opt.group_id,
                                 auto_offset_reset=self._opt.auto_offset_reset,
                                 enable_auto_commit=True,
                                 consumer_timeout_ms=5000)
        self.logger = get_logger('Kafka_consumer')

    def pop(self):
        result = []
        for data in self._kc:
            try:
                v = defaultdict(None, json.loads(data.value))
            except Exception as e:
                self.logger.info('topic: {}, offset: {} -> {}... pass...'
                                 .format(data.topic, data.offset, data.timestamp, e))
                continue
            datatime = data.timestamp
            result.append({'value': v, 'datatime': datatime})
        self.logger.info('Get {} data... from [{}]'.format(len(result), self._opt.topic))
        return result


class Kafka_queue_producer():
    def __init__(self, opt):
        self._opt = opt
        self._topic = self._opt.topic
        self._kp = KafkaProducer(bootstrap_servers=self._opt.bootstrap_servers,
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        self.logger = get_logger('Kafka_consumer')

    def push(self, data):
        data = [data] if isinstance(data, dict) else data
        for d in data:
            self._kp.send(self._topic, d)
        self.logger.info('send {} data... to [{}]'.format(len(data), self._opt.topic))
