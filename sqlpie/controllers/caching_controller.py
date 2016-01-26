# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Response
import json
import sqlpie

class CachingController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_initialize(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        capacity = json_data["capacity"] if "capacity" in json_data else 500
        auto_flush = True if "auto_flush" in json_data and json_data["auto_flush"] else False
        sqlpie.global_cache[bucket] = sqlpie.Caching(bucket, capacity, auto_flush)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_add(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "key" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        key = json_data["key"]
        expires_at = json_data["expires_at"] if "expires_at" in json_data else False
        if bucket not in sqlpie.global_cache:
            raise sqlpie.CustomException(sqlpie.CustomException.CACHE_IS_EMPTY)
        cache = sqlpie.global_cache[bucket]
        cache.add(key, expires_at)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_put(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "key" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "value" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        key = json_data["key"]
        value = json_data["value"]
        expires_at = json_data["expires_at"] if "expires_at" in json_data else False
        if bucket not in sqlpie.global_cache:
            raise sqlpie.CustomException(sqlpie.CustomException.CACHE_IS_EMPTY)
        cache = sqlpie.global_cache[bucket]
        cache.put(key, value, expires_at)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_get(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "key" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        key = json_data["key"]
        if bucket not in sqlpie.global_cache:
            raise sqlpie.CustomException(sqlpie.CustomException.CACHE_IS_EMPTY)
        cache = sqlpie.global_cache[bucket]
        value = cache.get(key)
        return {'success': True, 'bucket': bucket, 'key': key, 'value': value}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_remove(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        if bucket not in sqlpie.global_cache:
            raise sqlpie.CustomException(sqlpie.CustomException.CACHE_IS_EMPTY)
        cache = sqlpie.global_cache[bucket]
        if "key" in json_data:
            key = json_data["key"]
            cache.remove(key)
        else:
            cache.remove()
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_flush(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        if bucket not in sqlpie.global_cache:
            raise sqlpie.CustomException(sqlpie.CustomException.CACHE_IS_EMPTY)
        cache = sqlpie.global_cache[bucket]
        cache.flush()
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_reset(request):
        sqlpie.Cache().reset()
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def caching_destroy(request):
        json_data = request.get_json()
        if not "bucket" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        bucket = json_data["bucket"]
        if bucket not in sqlpie.global_cache:
            raise sqlpie.CustomException(sqlpie.CustomException.CACHE_IS_EMPTY)
        cache = sqlpie.global_cache[bucket]
        cache.remove()
        del sqlpie.global_cache[bucket]
        return {'success': True}
