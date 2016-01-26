# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Response
import json
import sqlpie

class SummarizationController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def service_summarization(request):
        json_data = request.get_json()
        if "bucket" in json_data and "documents" in json_data and \
          sqlpie.Predicate.convert_type(json_data["documents"], False) == sqlpie.Predicate.IS_LIST:
            bucket = json_data["bucket"]
            document_ids = json_data["documents"]
            documents = []
        elif "bucket" not in json_data and "documents" in json_data and \
          sqlpie.Predicate.convert_type(json_data["documents"], False) == sqlpie.Predicate.IS_LIST:
            bucket = None
            document_ids = None
            documents = json_data["documents"]
        else:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)

        options = {}
        if "options" in json_data:
            json_options = json_data["options"]
            if "max_sentences" in json_options and str(json_options["max_sentences"]) == str(int(json_options["max_sentences"])):
                options["max_sentences"] = json_options["max_sentences"]
            if "max_summary_size" in json_options and str(json_options["max_summary_size"]) == str(int(json_options["max_summary_size"])):
                options["max_summary_size"] = json_options["max_summary_size"]
            if "max_summary_percent" in json_options and str(json_options["max_summary_percent"]) == int(json_options["max_summary_percent"]):
                options["max_summary_percent"] = json_options["max_summary_percent"]
            if "max_keywords" in json_options and str(json_options["max_keywords"]) == int(json_options["max_keywords"]):
                options["max_keywords"] = json_options["max_keywords"]
            if "fields_to_summarize" in json_options:
                options["fields_to_summarize"] = json_options["fields_to_summarize"]

        engine = sqlpie.Summarizer(bucket, document_ids, documents)
        results = engine.summarize(options)
        return {'success': True, 'results':results}
