# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Predicate(object):
    __tablename = "predicates"
    IS_FLOAT = 1
    IS_BOOLEAN = 2
    IS_UNICODE = 3
    IS_INT = 4
    IS_NONETYPE= 5
    IS_DICT = 6
    IS_LIST = 7

    def __init__(self, predicate):
        self.predicate = predicate.lower().strip()
        self.predicate_id = sqlpie.Util.to_sha1(self.predicate)

    def __repr__(self):
        return '<Predicate %r>' % (self.predicate)

    def increment(self):
        sql = "INSERT INTO " + self.__tablename + " (predicate, predicate_id) VALUES (%s, UNHEX(%s)) "
        sql = sql + " ON DUPLICATE KEY UPDATE observation_count = observation_count + 1"
        g.cursor.execute(sql, (self.predicate, self.predicate_id))

    @staticmethod
    def convert_type(value, is_content_type=False):
        if is_content_type:
            content_type = value
        else:
            content_type = type(value).__name__
        resp = 0 # unknown
        if content_type == "float":
            resp = 1
        elif content_type == "bool":
            resp = 2
        elif content_type == "unicode":
            resp = 3
        elif content_type == "int":
            resp = 4
        elif content_type == "NoneType":
            resp = 5
        elif content_type == "dict":
            resp = 6
        elif content_type == "list":
            resp = 7
        return resp

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Predicate.__tablename,)
        g.cursor.execute(sql)
