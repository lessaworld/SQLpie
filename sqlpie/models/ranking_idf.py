# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class RankingIDF(object):
    __tablename = "ranking_idf"

    def __init__(self, bucket_id, term_id):
        self.bucket_id = bucket_id
        self.term_id = term_id

    def increment(self):
        sql = "INSERT INTO " + self.__tablename + " (bucket_id, term_id) VALUES (UNHEX(%s), UNHEX(%s)) "
        sql = sql + " ON DUPLICATE KEY UPDATE num_doc = num_doc + 1"
        g.cursor.execute(sql, (self.bucket_id, self.term_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def update_idf(bucket_id):
        sql = "UPDATE ranking_idf INNER JOIN buckets ON ranking_idf.bucket_id = buckets.bucket_id "
        sql = sql + " SET ranking_idf.frequency = 1 + IFNULL(LOG(buckets.doc_count / ranking_idf.num_doc),0) "
        sql = sql + " WHERE ranking_idf.bucket_id = UNHEX(%s)"
        g.cursor.execute(sql, (bucket_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (RankingIDF.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
