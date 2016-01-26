# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Bucket(object):
    __tablename = "buckets"
    DEFAULT = "default"

    def __init__(self, bucket):
        self.bucket = bucket.lower().strip()
        self.bucket_id = sqlpie.Util.to_sha1(self.bucket)

    def __repr__(self):
        return '<Bucket %r>' % (self.bucket)

    def increment(self):
        sql = "INSERT INTO " + self.__tablename + " (bucket, bucket_id) VALUES (%s, UNHEX(%s)) "
        sql = sql + " ON DUPLICATE KEY UPDATE doc_count = doc_count + 1"
        g.cursor.execute(sql, (self.bucket, self.bucket_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Bucket.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def decrement(bucket_id, num_docs):
        sql = "UPDATE " + Bucket.__tablename + " SET doc_count = doc_count - %s WHERE bucket_id = UNHEX(%s)"
        g.cursor.execute(sql, (num_docs, bucket_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
