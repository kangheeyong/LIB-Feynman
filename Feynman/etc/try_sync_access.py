import os
import time
import fcntl

import asyncio

from .util import get_logger


class Try_sync_access:
    def __init__(self, fname):
        self.fname = fname
        self.logger = get_logger('try_sync_access')
        self.sleep_t = 2

    def __enter__(self):
        while True:
            try:
                fd = os.open(self.fname, os.O_CREAT)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.fd = fd
                break
            except OSError:
                os.close(fd)
                self.logger.info('Waiting to release {}'.format(self.fname))
                time.sleep(self.sleep_t)

    def __exit__(self, exc_type, exc_value, traceback):
        # fcntl.flock(self.fd, fcntl.LOCK_UN)
        os.remove(self.fname)
        os.close(self.fd)

    async def __aenter__(self):
        while True:
            try:
                fd = os.open(self.fname, os.O_CREAT)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.fd = fd
                break
            except OSError:
                os.close(fd)
                self.logger.info('Waiting to release {}'.format(self.fname))
                await asyncio.sleep(self.sleep_t)

    async def __aexit__(self, exc_type, exc_value, traceback):
        # fcntl.flock(self.fd, fcntl.LOCK_UN)
        os.remove(self.fname)
        os.close(self.fd)
