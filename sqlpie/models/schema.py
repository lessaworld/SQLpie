# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Schema(object):
    __tablename = "`schema`"

    @staticmethod
    def get():
        sql = "SELECT version FROM " + Schema.__tablename + " ORDER BY id desc LIMIT 1"
        g.cursor.execute(sql, )
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        db_record = g.cursor.fetchone()
        response = None
        if db_record:
            response = db_record[0]
        return response
