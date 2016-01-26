# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Response
import json
import sqlpie

class MatchingController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def matching(request=None):
        json_data = request.get_json()
        results = []
        if "num_results" in json_data:
            num_results = int(json_data["num_results"])
        else:
            num_results = 1

        if "filter_query" in json_data:
            filter_query = json_data["filter_query"]
        else:
            filter_query = ""

        if "output_predicate" in json_data:
            output_predicate = json_data["output_predicate"]
        else:
            output_predicate = None

        valid_keys = ["num_results", "filter_query", "output_predicate", "bucket", "document_id", "search_bucket", "document"]
        if not all(k in valid_keys for k in json_data.keys()):
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        elif ("bucket" in json_data and "document_id" in json_data and "search_bucket" in json_data) and not \
            (len(json_data["bucket"].strip()) == 0 or len(json_data["document_id"].strip()) == 0 or
                len(json_data["search_bucket"].strip()) == 0):
            bucket = json_data["bucket"]
            document_id = json_data["document_id"]
            search_bucket = json_data["search_bucket"]
            matcher = sqlpie.Matcher()
            results = matcher.match_single(bucket, document_id, search_bucket, num_results, filter_query)
            resp = {'success': True, 'results': results}
        elif ("bucket" in json_data and (not "document_id" in json_data) and "search_bucket" in json_data) and not \
            (len(json_data["bucket"].strip()) == 0 or len(json_data["search_bucket"].strip()) == 0):
            bucket = json_data["bucket"]
            search_bucket = json_data["search_bucket"]
            matcher = sqlpie.Matcher()
            total_matches, output_predicate = matcher.match_all(bucket, search_bucket, num_results, filter_query, output_predicate)
            resp = {'success': True, 'total_matches': total_matches, 'output_predicate': output_predicate}
        elif ("document" in json_data) and ("search_bucket" in json_data) and len(unicode(json_data["document"]).strip()) > 0 and len(json_data["search_bucket"].strip()) > 0:
            document = json_data["document"]
            search_bucket = json_data["search_bucket"]
            matcher = sqlpie.Matcher()
            results = matcher.match_document(document, search_bucket, num_results, filter_query)
            resp = {'success': True, 'results': results}
        else:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)

        return resp

