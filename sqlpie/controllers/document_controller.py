# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

The DocumentController class handles all the routes associated with Documents (i.e. put, get, and remove.)

"""

from flask import g, Response
import json, sys, traceback
import sqlpie

class DocumentController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def put(request):
        record_count = 0
        json_data = request.get_json()
        if not "documents" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        documents = json_data["documents"]
        parsers = []
        if "options" in json_data:
            options = json_data["options"]
            if sqlpie.Document.PARSERS_PARAM in options:
                parsers = options[sqlpie.Document.PARSERS_PARAM]
        if isinstance(documents, dict):
            d = sqlpie.Document(documents,parsers)
            d.add()
            record_count = 1
        elif isinstance(documents, list):
            documents_to_process = []
            for doc in documents:
                documents_to_process.append(sqlpie.Document(doc,parsers))
            sqlpie.Document.add_multiple(documents_to_process)
            record_count = len(documents_to_process)
        else:
            pass
        return {'success': True, 'record_count': record_count}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def get(request):
        json_data = request.get_json()
        if not sqlpie.Document.ID_FIELD in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if sqlpie.Document.BUCKET_FIELD in json_data:
            bucket = json_data[sqlpie.Document.BUCKET_FIELD]
        else:
            bucket = sqlpie.Bucket.DEFAULT
        bucket_id = sqlpie.Bucket(bucket).bucket_id
        identifier = sqlpie.Util.to_sha1(unicode(json_data[sqlpie.Document.ID_FIELD]))
        d = sqlpie.Document.get(bucket_id, identifier)
        if not d:
            raise sqlpie.CustomException(sqlpie.CustomException.RECORD_NOT_FOUND)
        return {'success': True, 'document': d.document}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def remove(request):
        json_data = request.get_json()
        if not sqlpie.Document.ID_FIELD in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if sqlpie.Document.BUCKET_FIELD in json_data:
            bucket = json_data[sqlpie.Document.BUCKET_FIELD]
        else:
            bucket = sqlpie.Bucket.DEFAULT
        bucket_id = sqlpie.Bucket(bucket).bucket_id
        identifier = sqlpie.Util.to_sha1(unicode(json_data[sqlpie.Document.ID_FIELD]))
        removed = sqlpie.Document.remove(bucket_id, identifier)
        if not removed:
            raise sqlpie.CustomException(sqlpie.CustomException.RECORD_NOT_FOUND)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def reset(request):
        sqlpie.Bucket.reset()
        sqlpie.Document.reset()
        return {'success': True}
