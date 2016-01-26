# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceTagCloudTests(object):
    #
    # Service Tag Cloud Tests
    #

    def run_before_service_tagcloud_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        books = {"documents":[{"_id":"Back to the Future", "_bucket":"movies","name":"Back to the Future"},{"_id":"Iron Eagle", "_bucket":"movies","name":"Iron Eagle"},{"_id":"1492", "_bucket":"movies","name":"1492"},{"_id":"The Avengers", "_bucket":"movies","name":"The Avengers"},{"_id":"The Matrix", "_bucket":"movies","name":"The Matrix"}, {"_id":"Terminator", "_bucket":"movies","name":"Terminator"},{"_id":"Star Wars", "_bucket":"movies","name":"Star Wars"},{"_id":"The Goonies", "_bucket":"movies","name":"The Goonies"},{"_id":"Iron Man", "_bucket":"movies","name":"Iron Man"},{"_id":"Iron Curtain", "_bucket":"movies","name":"Iron Curtain"},{"_id":"Eagle of Iron", "_bucket":"movies","name":"Eagle of Iron"},{"_id":"Eagle of Iron Eagle", "_bucket":"movies","name":"Eagle of Iron Eagle Eagle Eagle Eagle"}]}
        response = self.app.post('/document/put', data=json.dumps(books), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def test_service_tagcloud_01_relevance(self):
        self.run_before_service_tagcloud_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Eagle _bucket:movies", "tagcloud":"relevance"}), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'Eagle _bucket:movies', u'tags': [{u'term_count': 7, u'term': u'eagle', u'_score': 8.35203, u'num_docs': 3}, {u'term_count': 5, u'term': u'iron', u'_score': 2.813203, u'num_docs': 5}]}, "Actual Response : %r" % json_response

    def test_service_tagcloud_02_frequency(self):
        self.run_before_service_tagcloud_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Eagle _bucket:movies", "tagcloud":"frequency"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'Eagle _bucket:movies', u'tags': [{u'term_count': 5, u'term': u'iron', u'_score': 2.813203, u'num_docs': 5}, {u'term_count': 7, u'term': u'eagle', u'_score': 8.35203, u'num_docs': 3}]}, "Actual Response : %r" % json_response

    def test_service_tagcloud_03_max_results(self):

        self.run_before_service_tagcloud_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Eagle _bucket:movies", "tagcloud":"frequency", "num":1}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True , "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'Eagle _bucket:movies', u'tags': [{u'term_count': 5, u'term': u'iron', u'_score': 2.813203, u'num_docs': 5}]}, "Actual Response : %r" % json_response

    def test_service_tagcloud_04_max_results(self):

        self.run_before_service_tagcloud_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Eagle _bucket:movies", "tagcloud":"frequency", "num":2}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["tags"]) == 2, "Actual Response : %r" % json_response
