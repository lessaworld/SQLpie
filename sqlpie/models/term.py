# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Term(object):
    __tablename = "terms"

    def __init__(self, bucket_id, term):
        self.bucket_id = bucket_id
        self.term = term
        self.term_id = sqlpie.Util.to_sha1(self.term)

    def increment(self):
        sql = "INSERT INTO " + self.__tablename + " (bucket_id, term_id) VALUES (UNHEX(%s), UNHEX(%s)) "
        sql = sql + " ON DUPLICATE KEY UPDATE term_count = term_count + 1"
        g.cursor.execute(sql, (self.bucket_id, self.term_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def get_key(term):
        return sqlpie.Util.to_sha1(sqlpie.Indexer.normalize_term(term))

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Term.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
