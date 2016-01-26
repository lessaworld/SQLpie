# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class RankingTF(object):
    __tablename = "ranking_tf"

    def __init__(self, bucket_id, document_id, term_id, normalized_frequency):
        self.bucket_id = bucket_id
        self.document_id = document_id
        self.term_id = term_id
        self.normalized_frequency  = normalized_frequency

    def add(self):
        sql = "INSERT INTO " + self.__tablename + " (bucket_id, document_id, term_id, normalized_frequency) "
        sql = sql + " VALUES (UNHEX(%s), UNHEX(%s), UNHEX(%s), %s) "
        g.cursor.execute(sql, (self.bucket_id, self.document_id, self.term_id, self.normalized_frequency))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (RankingTF.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
