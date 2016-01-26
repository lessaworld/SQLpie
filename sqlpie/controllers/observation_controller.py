# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

The ObservationController class handles all the routes associated with Observations (i.e. put, ...)

"""

from flask import Response
import json
import sqlpie

class ObservationController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def put(request):
        json_data = request.get_json()
        record_count = 0
        if isinstance(json_data, dict):
            e = sqlpie.Observation(json_data)
            e.add()
            record_count = 1
        elif isinstance(json_data, list):
            observations_to_process = []
            for observation in json_data:
                observations_to_process.append(sqlpie.Observation(observation))
            sqlpie.Observation.add_multiple(observations_to_process)
            record_count = len(observations_to_process)
        else:
            pass
        return {'success': True, 'record_count': record_count}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def remove(request):
        json_data = request.get_json()
        record_count = sqlpie.Observation.remove(json_data)
        return {'success': True, 'record_count': record_count}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def get(request):
        json_data = request.get_json()
        observations, total = sqlpie.Observation.get(json_data)
        return {'success': True, 'observations': observations, 'record_count': len(observations), 'total_count':total}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def reset(request):
        sqlpie.Observation.reset()
        sqlpie.Predicate.reset()
        return {'success': True}
