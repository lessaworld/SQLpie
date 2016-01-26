# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceIndexerTests(object):
    #
    # Service Indexer Tests
    #

    def run_before_service_indexer_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        books = {"documents":[{"_id":"Back to the Future", "_bucket":"movies","name":"Back to the Future"},{"_id":"Iron Eagle", "_bucket":"movies","name":"Iron Eagle"},{"_id":"1492", "_bucket":"movies","name":"1492"},{"_id":"The Avengers", "_bucket":"movies","name":"The Avengers"},{"_id":"The Matrix", "_bucket":"movies","name":"The Matrix"}, {"_id":"Terminator", "_bucket":"movies","name":"Terminator"},{"_id":"Star Wars", "_bucket":"movies","name":"Star Wars"},{"_id":"The Goonies", "_bucket":"movies","name":"The Goonies"},{"_id":"Iron Man", "_bucket":"movies","name":"Iron Man"},{"_id":"Iron Curtain", "_bucket":"movies","name":"Iron Curtain"},{"_id":"Eagle of Iron", "_bucket":"movies","name":"Eagle of Iron"}]}
        response = self.app.post('/document/put', data=json.dumps(books), content_type = 'application/json')

    def test_service_index(self):
        self.run_before_service_indexer_tests()

        request =[]
        response = self.app.post('/service/index', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response