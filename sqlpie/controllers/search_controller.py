# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Response
import json
import sqlpie

class SearchController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def service_index(request=None):
        rebuild = False
        json_data = request.get_json()
        if "options" in json_data:
            options = json_data["options"]
            if sqlpie.Indexer.REBUILD_PARAM in options:
                rebuild = options[sqlpie.Indexer.REBUILD_PARAM]

        if rebuild:
            sqlpie.Indexer.rebuild()
        sqlpie.Indexer().index_documents()
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def service_search(request):
        json_data = request.get_json()
        query, tagcloud_search, geo_radius_search, geo_target_search = "", "", "", ""
        geo_sort_by = sqlpie.Searcher.SORT_BY_DISTANCE
        is_tagcloud_search = False
        is_geo_search = False
        num_results = 10
        start_result = 0

        if sqlpie.Searcher.QUERY_OPERATOR in json_data:
            query = json_data[sqlpie.Searcher.QUERY_OPERATOR]
        if sqlpie.Searcher.TAGCLOUD_OPERATOR in json_data:
            tagcloud_search = json_data[sqlpie.Searcher.TAGCLOUD_OPERATOR].lower()
        if sqlpie.Searcher.GEO_RADIUS_OPERATOR in json_data:
            geo_radius_search = json_data[sqlpie.Searcher.GEO_RADIUS_OPERATOR]
        if sqlpie.Searcher.GEO_TARGET_OPERATOR in json_data:
            geo_target_search = json_data[sqlpie.Searcher.GEO_TARGET_OPERATOR].lower()
        if sqlpie.Searcher.GEO_SORT_BY in json_data:
            geo_sort_by = json_data[sqlpie.Searcher.GEO_SORT_BY].lower()
        if sqlpie.Searcher.NUM_RESULTS in json_data:
            num_results = int(json_data[sqlpie.Searcher.NUM_RESULTS])
        if sqlpie.Searcher.START_RESULT in json_data:
            start_result = int(json_data[sqlpie.Searcher.START_RESULT])

        if tagcloud_search:
            if not tagcloud_search in [sqlpie.Searcher.SORT_TAGCLOUD_BY_RELEVANCE, \
                                      sqlpie.Searcher.SORT_TAGCLOUD_BY_FREQUENCY]:
                raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
            else:
                is_tagcloud_search = True
        if geo_radius_search or geo_target_search:
            if not sqlpie.Util.is_number(geo_radius_search) or not geo_radius_search or \
                not geo_target_search or not len(geo_target_search.split(",")) == 2 or \
                not sqlpie.Util.is_number(geo_target_search.split(",")[0]) or \
                not sqlpie.Util.is_number(geo_target_search.split(",")[1]) or \
                geo_sort_by not in [sqlpie.Searcher.SORT_BY_RELEVANCE, sqlpie.Searcher.SORT_BY_DISTANCE]:
                raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
            else:
                is_geo_search = True

        engine = sqlpie.Searcher(query)
        if is_tagcloud_search:
            results = engine.run_tagcloud(tagcloud_search, num_results)
        elif is_geo_search:
            results = engine.run_geosearch(geo_radius_search, geo_target_search, num_results, start_result, geo_sort_by)
        else:
            results = engine.run_searcher(num_results, start_result)

        return {'success': True, 'results':results}
