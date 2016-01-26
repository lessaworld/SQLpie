# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

Thread safe cache class

"""

from flask import g
import sqlpie
from collections import OrderedDict
from threading import Lock
import time

class Caching(object):
    def __init__(self,bucket=sqlpie.Bucket.DEFAULT,capacity=500,auto_flush=False):
        self.bucket = bucket
        try:
            self.capacity = int(capacity)
        except:
            self.capacity = 500
        self.auto_flush = auto_flush
        self.cache_lock = Lock()
        self.cache = OrderedDict()
        self.dirty = {}
        self._load()

    def get(self,key):
        key_id = sqlpie.Cache.convert_to_hash_key(key)
        now = time.time()
        ret = None
        with self.cache_lock:
            if self.cache.has_key(key_id):
                v = self.cache[key_id]
                if len(v) == 3:
                    cache_key, value, expire_at = self.cache[key_id]
                    if expire_at > now:
                        ret = value
                    else:
                        self.dirty[key_id] = 0
                        if self.auto_flush:
                            self.flush(locked=True)
                        del self.cache[key_id]
                else:
                    ret = self.cache[key_id][1]
        return ret

    def add(self, key, expire_at=False):
        self.put(key, key, expire_at)

    def put(self,key,value,expire_at=False):
        try:
            expire_at = int(expire_at)
        except:
            expire_at = False

        key_id = sqlpie.Cache.convert_to_hash_key(key)
        now = time.time()
        with self.cache_lock:
            while len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            if not expire_at:
                self.cache[key_id] = (key, value,)
            else:
                self.cache[key_id] = (key, value, now + expire_at)
            self.dirty[key_id] = 1
        if self.auto_flush:
            self.flush()

    def remove(self,key=None):
        with self.cache_lock:
            if key:
                key_id = sqlpie.Cache.convert_to_hash_key(key)
                if self.cache.has_key(key_id):
                    del self.cache[key_id]
                    self.dirty[key_id] = 0
                else:
                    raise sqlpie.CustomException(sqlpie.CustomException.CACHE_KEY_NOT_FOUND)
            else:
                sqlpie.Cache.remove(self.bucket)
                self.cache = OrderedDict()
                self.dirty = {}
        if self.auto_flush:
            self.flush()

    def flush(self,locked=False):
        # sync data to database
        #
        def _flush():
            for k in self.dirty.keys():
                v = self.dirty[k]
                if v == 1:
                    # do insert/update for cached_bucket = self.bucket
                    if k in self.cache:
                        value = self.cache[k]
                        if len(value) == 3:
                            cache_key, value, expire_at = self.cache[k]
                        else:
                            cache_key, value, expire_at = value[0], value[1], None
                        c = sqlpie.Cache(self.bucket, cache_key, value, expire_at)
                        c.add()
                elif v == 0:
                    # do delete for cached_bucket = self.bucket
                    sqlpie.Cache.remove(self.bucket, k)
                else:
                    pass
            self.dirty.clear()

        if locked:
            _flush()
        else:
            with self.cache_lock:
                _flush()

    @staticmethod
    def reset():
        sqlpie.Cache.reset()

    # private

    def _load(self):
        # load data for cached_bucket = self.bucket
        # if the bucket doesn't exist, do nothing.
        try:
            r = sqlpie.Cache.get(self.bucket)
            with self.cache_lock:
                for c in r:
                    key, cache_key, value, expire_at = c[1], c[3], c[4], c[2]
                    if expire_at:
                        self.cache[key] = (cache_key, value, time.mktime(expire_at.timetuple()))
                    else:
                        self.cache[key] = (cache_key, value,)
        except:
            pass