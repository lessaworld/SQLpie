# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""
from flask import g, Response
import json, sys, traceback
import os
from functools import wraps
import sqlpie

class BaseController(object):

    @staticmethod
    def controller_wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                g.conn.begin()
                data = f(*args, **kwargs)
                g.conn.commit()
                http_status = 200
            except sqlpie.CustomException as e:
                if sqlpie.Util.is_debug():
                    traceback.print_tb(sys.exc_info()[2])
                data = {'success': False, 'err':unicode(e)}
                http_status = 400
                try:
                    g.conn.commit()
                except:
                    pass
            except Exception as e:
                if sqlpie.Util.is_debug():
                    traceback.print_tb(sys.exc_info()[2])
                    data = {'success': False, 'err':unicode(e), 'traceback':traceback.extract_tb(sys.exc_info()[2])}
                else:
                    data = {'success': False, 'err':unicode(e)}
                http_status = 500
                try:
                    g.conn.rollback()
                except:
                    pass
            if sqlpie.Config.get(sqlpie.Config.OUTPUT_JSON_BYTESTRINGS):
                data = sqlpie.Util.json_unicode_to_bytes(data) # handle escaping quotes
            if sqlpie.Util.is_debug():
                json_data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            else:
                json_data = json.dumps(data)
            if sqlpie.Config.get(sqlpie.Config.OUTPUT_JSON_BYTESTRINGS):
                json_data = json_data.decode('unicode-escape')
            return Response(json_data, status=http_status, mimetype='application/json;charset=utf-8')
        return decorated_function


