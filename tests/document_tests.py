# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class DocumentTests(object):

    #
    # Document Tests
    #

    def test_document_01_put_multiple(self):
        request = {"documents":[{"_id":"001", "_bucket":"customers", "name":"John"},{"_id":"002", "_bucket":"customers", "name":"Peter"},{"_id":"003", "_bucket":"customers", "name":"Thomas"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 3, "Actual Response : %r" % json_response

    def test_document_02_get_success(self):
        request = {"documents":[{"_id":"004", "_bucket":"customers", "name":"John"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')

        request = {"_id":"004", "_bucket":"customers"}
        response = self.app.post('/document/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        test_doc = json_response["document"]
        assert test_doc["_id"] == "004", "Actual Response : %r" % json_response
        assert test_doc["_bucket"] == "customers", "Actual Response : %r" % json_response
        assert test_doc["name"] == "John", "Actual Response : %r" % json_response

    def test_document_03_get_fail(self):
        request = {"_id":"004e"}
        response = self.app.post('/document/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert json_response["err"] == sqlpie.CustomException.RECORD_NOT_FOUND, "Actual Response : %r" % json_response

    def test_document_04_remove_success(self):
        request = {"documents":[{"_id":"005", "_bucket":"customers", "name":"John"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')

        request = {"_id":"005", "_bucket":"customers"}
        response = self.app.post('/document/remove', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        response = self.app.post('/document/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert json_response["err"] == sqlpie.CustomException.RECORD_NOT_FOUND, "Actual Response : %r" % json_response

    def test_document_05_remove_fail(self):
        request = {"documents":[{"_id":"006", "_bucket":"customers", "name":"John"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')

        request = {"_id":"006e", "_bucket":"customers"}
        response = self.app.post('/document/remove', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert json_response["err"] == sqlpie.CustomException.RECORD_NOT_FOUND, "Actual Response : %r" % json_response

        request = {"_id":"006", "_bucket":"customers"}
        response = self.app.post('/document/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

    def test_document_06_reset(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

    def test_document_07_put_single(self):
        request = {"documents":{"_id":"010", "_bucket":"customers", "name":"James"}}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 1, "Actual Response : %r" % json_response

    def run_before_service_parser_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        employees = {"documents":[{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA","title":"CEO"},{"_id":"002", "_bucket":"employees","name":"Peter","location":"Cleveland, OH","title":"CFO"},{"_id":"003", "_bucket":"employees","name":"Jeff","location":"Wexford, PA", 'title': "Team Lead"},{"_id":"004", "_bucket":"employees","name":"Beth","location":"Los Angeles, CA"},{"_id":"005", "_bucket":"employees","name":"Jack","location":"Bethel Park, PA","title":"Chief Marketing Officer"},{"_id":"006", "_bucket":"employees","name":"Mike","location":"Monroeville, PA"},{"_id":"007", "_bucket":"employees","name":"Nancy","location":"Chicago, IL", 'title': "Software Engineer"},{"_id":"008", "_bucket":"employees","name":"Anne","location":"Philadelphia, PA","title":"COO"}], "options":{"parsers":["sample"]}}
        response = self.app.post('/document/put', data=json.dumps(employees), content_type = 'application/json')

    def test_document_08_get_parsed_document(self):
        self.run_before_service_parser_tests()

        request = {"_id":"001", "_bucket":"employees"}
        response = self.app.post('/document/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["document"] == {u'name': u'John', u'title': u'CEO', u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'is_c_level': True, u'latitude': 40.4405556, u'_id': u'001'}, "Actual Response : %r" % json_response
