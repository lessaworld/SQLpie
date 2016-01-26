# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Cache(object):
    __tablename = "caches"

    def __init__(self, bucket, key, value=None, expire_at=None):
        self.bucket_name = bucket
        b = sqlpie.Bucket(bucket)
        self.bucket_id = b.bucket_id
        self.key_id = sqlpie.Cache.convert_to_hash_key(key)
        self.key = key # key[0:2047] if len(key) > 2048 else key
        self.value = value #value[0:2047] if len(value) > 2048 else value
        if expire_at:
            self.expire_at = sqlpie.Util.get_current_utc_from_timestamp(expire_at)
        else:
            self.expire_at = sqlpie.Util.get_current_utc_timestamp()

    def __repr__(self):
        return '<Cache %r %r>' % (self.bucket_name, self.key)

    def add(self):
        sql =  "INSERT INTO " + self.__tablename + " (bucket_id, key_id, expire_at, cache_key, value) VALUES "
        sql += "(UNHEX(%s), UNHEX(%s), %s, %s, %s) "
        sql += " ON DUPLICATE KEY UPDATE expire_at = %s, value = %s"
        g.cursor.execute(sql, (self.bucket_id, self.key_id, self.expire_at, self.key, self.value, self.expire_at, self.value))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        g.conn.commit()

    @staticmethod
    def get(bucket, key=None):
        b = sqlpie.Bucket(bucket)
        bucket_id = b.bucket_id
        sql = "SELECT HEX(bucket_id), HEX(key_id), expire_at, cache_key, value FROM "
        if key:
            key_id = sqlpie.Cache.convert_to_hash_key(key)
            sql += Cache.__tablename + " WHERE bucket_id = UNHEX(%s) and key_id = UNHEX(%s) LIMIT 1"
            g.cursor.execute(sql, (bucket_id, key_id,))
            if sqlpie.Util.is_debug():
                print g.cursor._executed
            r = g.cursor.fetchone()
        else:
            sql += Cache.__tablename + " WHERE bucket_id = UNHEX(%s)"
            g.cursor.execute(sql, (bucket_id,))
            if sqlpie.Util.is_debug():
                print g.cursor._executed
            r = g.cursor.fetchall()
        return r

    @staticmethod
    def remove(bucket, key_id=None):
        b = sqlpie.Bucket(bucket)
        bucket_id = b.bucket_id
        sql = "DELETE FROM "
        sql += Cache.__tablename + " WHERE bucket_id = UNHEX(%s)"
        params = (bucket_id,)
        if key_id:
            sql += " and key_id = UNHEX(%s) LIMIT 1"
            params = (bucket_id, key_id,)
        g.cursor.execute(sql, params)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        sql = "SELECT ROW_COUNT() "
        g.cursor.execute(sql)
        data = g.cursor.fetchone()
        return data[0]

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Cache.__tablename,)
        g.cursor.execute(sql)

    @staticmethod
    def convert_to_hash_key(key):
        return sqlpie.Util.to_sha1(key.lower().strip())
