import _pickle

from feynman.etc import Try_sync_access
from feynman.etc.util import get_logger


class Pickle_serializer():
    def __init__(self):
        self.logger = get_logger()

    def load(self, fname):
        with Try_sync_access(fname + '.lock'):
            with open(fname, "rb") as f:
                data = _pickle.load(f)
        self.logger.info('Pickle load : {}'.format(fname))
        return data

    def dump(self, data, fname):
        with Try_sync_access(fname + '.lock'):
            with open(fname, "wb") as f:
                _pickle.dump(data, f)
        self.logger.info('Pickle dump : {}, {}'.format(fname, type(data)))
