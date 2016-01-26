# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Response
import json
import sqlpie

class CollaborativeController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def service_similarity(request):
        json_data = request.get_json()
        if "subject_bucket" in json_data and "subject_id" in json_data and \
            "object_bucket" in json_data and "object_id" not in json_data and \
            "predicate" in json_data:
            subject_bucket = json_data["subject_bucket"]
            object_bucket = json_data["object_bucket"]
            subject_id = json_data["subject_id"]
            object_id = None
            predicate = json_data["predicate"]
        elif "object_bucket" in json_data and "object_id" in json_data and \
            "subject_bucket" in json_data and "subject_id" not in json_data and \
            "predicate" in json_data:
            subject_bucket = json_data["subject_bucket"]
            object_bucket = json_data["object_bucket"]
            object_id = json_data["object_id"]
            subject_id = None
            predicate = json_data["predicate"]
        else:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)

        if "metric" in json_data:
            metric = json_data["metric"]
            if metric != "pearson" and metric != "manhattan":
                raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        else:
            metric = "pearson"

        if "limit" in json_data and str(json_data["limit"]) == int(json_data["limit"]):
            limit = json_data["limit"]
        else:
            limit = 10

        engine = sqlpie.Recommender(subject_bucket, object_bucket, subject_id, object_id, predicate)
        results = engine.similarity(limit, metric)
        return {'success': True, 'results':results}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def service_recommend(request):
        json_data = request.get_json()
        if "subject_bucket" in json_data and "subject_id" in json_data and \
            "object_bucket" in json_data and "object_id" not in json_data and \
            "predicate" in json_data:
            subject_bucket = json_data["subject_bucket"]
            object_bucket = json_data["object_bucket"]
            subject_id = json_data["subject_id"]
            object_id = None
            predicate = json_data["predicate"]
        elif "object_bucket" in json_data and "object_id" in json_data and \
            "subject_bucket" in json_data and "subject_id" not in json_data and \
            "predicate" in json_data:
            subject_bucket = json_data["subject_bucket"]
            object_bucket = json_data["object_bucket"]
            object_id = json_data["object_id"]
            subject_id = None
            predicate = json_data["predicate"]
        else:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)

        if "metric" in json_data:
            metric = json_data["metric"]
            if metric != "pearson" and metric != "manhattan":
                raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        else:
            metric = "pearson"

        if "limit" in json_data and str(json_data["limit"]) == int(json_data["limit"]):
            limit = json_data["limit"]
        else:
            limit = 10

        engine = sqlpie.Recommender(subject_bucket, object_bucket, subject_id, object_id, predicate)
        results = engine.recommendation(limit, metric)
        return {'success': True, 'results':results}
