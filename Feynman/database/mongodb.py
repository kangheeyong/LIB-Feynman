import datetime

from pymongo import MongoClient

from ..etc.util import get_logger


class Mongodb():
    def __init__(self, opt):
        self._opt = opt
        self.logger = get_logger()
        self._client = MongoClient(self._opt.server)
        self._db = self._client[self._opt.database]
        self._collection = self._db[self._opt.collection]
        if self._opt.ttl_enable:
            self._ttl_set()
        for key, value in self._collection.index_information().items():
            self.logger.info('Index set [{}/{}/{}] -> {}:{}'.format(self._opt.server, self._opt.database, self._opt.collection, key, value))

    def _ttl_set(self):
        dic = self._collection.index_information()
        if 'ttl_1' not in dic:
            self._collection.create_index("ttl", expireAfterSeconds=self._opt.ttl_t)
        else:
            if dic['ttl_1']['expireAfterSeconds'] != self._opt.ttl_t:
                self._collection.drop_index('ttl_1')
                self._collection.create_index("ttl", expireAfterSeconds=self._opt.ttl_t)
                self.logger.info('TTL time change from {}s to {}s'.format(dic['ttl_1']['expireAfterSeconds'], self._opt.ttl_t))

    def insert(self, data):
        if not data:
            return
        data = [data] if isinstance(data, dict) else data
        ttl = datetime.datetime.utcnow()
        for datum in data:
            datum['ttl'] = ttl
        self._collection.insert_many(data)
        self.logger.info('Insert into [{}/{}/{}] -> {} data...'.format(self._opt.server, self._opt.database, self._opt.collection, len(data)))

    def find(self, data):
        return self._collection.find(data)
