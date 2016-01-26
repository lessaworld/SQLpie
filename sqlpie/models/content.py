# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Content(object):
    __tablename = "contents"

    def __init__(self, bucket_id, document_id, key_id, content_type, value):
        self.bucket_id = bucket_id
        self.document_id = document_id
        self.key_id = key_id
        self.content_type = self._content_type_convert(content_type)
        self.value = unicode(value)
        if self.content_type in [1,4]:
            self.numeric_value = value
        elif self.content_type == 2:
            if value.lower() == "true":
                self.numeric_value = 1
            else:
                self.numeric_value = 0
        else:
            date_value = sqlpie.Util.convert_to_date(value)
            if date_value:
                self.numeric_value = date_value
            else:
                self.numeric_value = None

    def __repr__(self):
        return '<Content %r>' % (self.key_id)

    def add(self):
        sql = "INSERT INTO " + self.__tablename
        sql += " (bucket_id, document_id, key_id, content_type, value, numeric_value) VALUES (UNHEX(%s), UNHEX(%s), UNHEX(%s), %s, %s, %s)"
        g.cursor.execute(sql, (self.bucket_id, self.document_id, self.key_id, self.content_type, self.value, self.numeric_value))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def _content_type_convert(self, content_type):
        resp = 0 # unknown (dict and list not currently being recorded)
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
        return resp

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Content.__tablename,)
        g.cursor.execute(sql)
