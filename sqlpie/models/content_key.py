# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class ContentKey(object):
    __tablename = "content_keys"

    def __init__(self, content_key):
        self.content_key = content_key
        self.key_id = sqlpie.Util.to_sha1(content_key)

    def __repr__(self):
        return '<ContentKey %r>' % (self.content_key)

    def increment(self):
        sql = "INSERT INTO " + self.__tablename + " (content_key, key_id) VALUES (%s, UNHEX(%s)) "
        sql = sql + " ON DUPLICATE KEY UPDATE key_count = key_count + 1"
        g.cursor.execute(sql, (self.content_key, self.key_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def flip(key):
        ck = ".".join(key.split(".")[::-1])
        if ck.endswith("."):
            ck = ck + "%%"
        else:
            ck = ck + "."
        return ck


    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (ContentKey.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
