# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Health(object):

    @staticmethod
    def db_name():
        sql = "SELECT DATABASE();"
        g.cursor.execute(sql)
        return g.cursor.fetchone()[0]
