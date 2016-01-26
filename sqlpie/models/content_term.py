# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class ContentTerm(object):
    __tablename = "content_terms"

    def __init__(self, bucket_id, document_id, key_id, term_id, term_pos, original):
        self.bucket_id = bucket_id
        self.document_id = document_id
        self.key_id = key_id
        self.term_id = term_id
        self.term_pos  = term_pos
        self.original = original

    def add(self):
        sql = "INSERT INTO " + self.__tablename + " (bucket_id, document_id, key_id, term_id, term_pos, original) "
        sql = sql + " VALUES (UNHEX(%s), UNHEX(%s), UNHEX(%s), UNHEX(%s), %s, %s) "
        g.cursor.execute(sql, (self.bucket_id, self.document_id, self.key_id, self.term_id, self.term_pos, self.original))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def    get_doc_ids(sql_conditions):
        sql = ""
        c_idx = 0
        for c in sql_conditions:
            if c_idx == 0:
                sql += "SELECT distinct HEX(idx%s.document_id) FROM " % (c_idx,) + ContentTerm.__tablename
                sql += " idx%s WHERE idx%s.term_id = UNHEX('%s') " % (c_idx, c_idx, c)
            else:
                sql += " AND exists (SELECT 1 FROM " + ContentTerm.__tablename + " idx%s WHERE idx%s.term_id = UNHEX('%s') " % (c_idx, c_idx, c)
                sql += " AND idx0.document_id = idx%s.document_id)" % (c_idx,)
            c_idx += 1
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed

        data = g.cursor.fetchall()
        doc_ids = []
        for row in data :
            doc_ids.append(row[0])
        return doc_ids

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (ContentTerm.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
