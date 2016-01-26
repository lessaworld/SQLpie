# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class GeoDocument(object):
    __tablename = "geo_documents"

    @staticmethod
    def add(bucket_id, document_id, latitude, longitude):
        sql = "INSERT INTO " + GeoDocument.__tablename
        sql += " (bucket_id, document_id, latitude, longitude) VALUES (UNHEX(%s), UNHEX(%s), %s, %s)"
        sql += " ON DUPLICATE KEY UPDATE latitude=%s, longitude=%s"
        g.cursor.execute(sql, (bucket_id, document_id, latitude, longitude, latitude, longitude))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def remove(bucket_id, document_id):
        sql = "DELETE FROM "
        sql += GeoDocument.__tablename + " WHERE bucket_id = UNHEX(%s) and document_id = UNHEX(%s) LIMIT 1"
        g.cursor.execute(sql, (bucket_id, document_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (GeoDocument.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
