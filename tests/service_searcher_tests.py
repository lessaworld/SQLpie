# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceSearcherTests(object):
    #
    # Service Searcher Tests
    #

    def run_before_service_searcher_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        books = {"documents":[{"_id":"Back to the Future", "_bucket":"movies","name":"Back to the Future"},{"_id":"Iron Eagle", "_bucket":"movies","name":"Iron Eagle"},{"_id":"1492", "_bucket":"movies","name":"1492"},{"_id":"The Avengers", "_bucket":"movies","name":"The Avengers"},{"_id":"The Matrix", "_bucket":"movies","name":"The Matrix"}, {"_id":"Terminator", "_bucket":"movies","name":"Terminator"},{"_id":"Star Wars", "_bucket":"movies","name":"Star Wars"},{"_id":"The Goonies", "_bucket":"movies","name":"The Goonies"},{"_id":"Iron Man", "_bucket":"movies","name":"Iron Man"},{"_id":"Iron Curtain", "_bucket":"movies","name":"Iron Curtain"},{"_id":"Eagle of Iron", "_bucket":"movies","name":"Eagle of Iron"},{"_id":"hp01", "_bucket":"movies","name":"Harry Potter"},{"_id":"hp02", "_bucket":"movies","name":"Harry Potter"},{"_id":"hp03", "_bucket":"movies","name":"Harry Potter"}]}
        response = self.app.post('/document/put', data=json.dumps(books), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def run_before_service_searcher_tests_unicode(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        docs = {"documents":[{"_id":"001", "_bucket":"tests","name":"Antonia's"},{"_id":"002", "_bucket":"tests","name":"Misérables"},{"_id":"003", "_bucket":"tests","name":"naïve"},{"_id":"004", "_bucket":"tests","name":"café"}]}
        response = self.app.post('/document/put', data=json.dumps(docs), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def run_before_service_searcher_tests_multiple_originals(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        docs = {"documents":[{"_id":"005", "_bucket":"tests","name":"Drive"},{"_id":"006", "_bucket":"tests","name":"Driving"},{"_id":"007", "_bucket":"tests","name":"driving"}]}
        response = self.app.post('/document/put', data=json.dumps(docs), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        docs = {"documents":[{"_id":"001", "_bucket":"orders","order_date":"Mar/01/2015", "billing":{"state":"pa", "city":"pittsburgh"}, "shipping":{"state":"ca", "city":"los angeles"}, "total": 250}, {"_id":"002", "_bucket":"orders","order_date":"Jul/12/2015", "billing":{"state":"pa", "city":"pittsburgh"}, "shipping":{"state":"ca", "city":"los angeles"}, "total": 200}, {"_id":"003", "_bucket":"orders","order_date":"Dec/01/2015", "billing":{"state":"fl", "city":"florida"}, "shipping":{"state":"ca", "city":"los angeles"}, "total": 300}, {"_id":"004", "_bucket":"orders","order_date":"Mar/15/2015", "billing":{"state":"pa", "city":"pittsburgh"}, "shipping":{"state":"ca", "city":"san francisco"}, "total": 450}, {"_id":"005", "_bucket":"orders","order_date":"Mar/01/2015", "billing":{"state":"pa", "city":"erie"}, "shipping":{"state":"fl", "city":"florida"}, "total": 50}, {"_id":"006", "_bucket":"orders","order_date":"Oct/01/2015", "billing":{"state":"pa", "city":"erie"}, "shipping":{"state":"fl", "city":"florida", "cost":84.32}, "total": 50}, {"_id":"007", "_bucket":"orders","order_date":"Oct/01/2015", "billing":{"state":"pa", "city":"erie"}, "shipping":{"state":"fl", "city":"florida", "cost":84.32, "shipping_date":"Oct/02/2015"}, "total": 50}
        ], "parsers":["dates"]}
        response = self.app.post('/document/put', data=json.dumps(docs), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def run_before_service_searcher_tests_boolean_field_search(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        docs = {"documents":[{"_id":"001", "_bucket":"orders","order_date":"Mar/01/2015", "billing":{"state":"pa", "city":"pittsburgh"}, "shipping":{"state":"ca", "city":"los angeles"}, "total": 250}, {"_id":"002", "_bucket":"orders","order_date":"Jul/12/2015", "billing":{"state":"pa", "city":"pittsburgh"}, "shipping":{"state":"ca", "city":"los angeles","shipped":True}, "total": 200}, {"_id":"003", "_bucket":"orders","order_date":"Dec/01/2015", "billing":{"state":"fl", "city":"florida"}, "shipping":{"state":"ca", "city":"los angeles"}, "total": 300}, {"_id":"004", "_bucket":"orders","order_date":"Mar/15/2015", "billing":{"state":"pa", "city":"pittsburgh"}, "shipping":{"state":"ca", "city":"san francisco"}, "total": 450}, {"_id":"005", "_bucket":"orders","order_date":"Mar/01/2015", "billing":{"state":"pa", "city":"erie"}, "shipping":{"state":"fl", "city":"florida"}, "total": 50}, {"_id":"006", "_bucket":"orders","order_date":"Oct/01/2015", "billing":{"state":"pa", "city":"erie"}, "shipping":{"state":"fl", "city":"florida", "cost":84.32, "shipped":False}, "total": 50}, {"_id":"007", "_bucket":"orders","order_date":"Oct/01/2015", "billing":{"state":"pa", "city":"erie"}, "shipping":{"state":"fl", "city":"florida", "cost":84.32, "shipping_date":"Oct/02/2015"}, "total": 50}
        ], "parsers":["dates"]}
        response = self.app.post('/document/put', data=json.dumps(docs), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def test_service_search_01_query_not_found(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"vnzzoasd3if"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 0, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 0, "Actual Response : %r" % json_response

    def test_service_search_02_query_wrong_bucket(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'"Iron Eagle"'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 0, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 0, "Actual Response : %r" % json_response

    def test_service_search_03_query_quote(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'"Iron Eagle" _bucket:movies'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_04_query_multiple(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Iron _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 4, "Actual Response : %r" % json_response

    def test_service_search_05_query_not_operator(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Iron -man _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 3, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 3, "Actual Response : %r" % json_response

    def test_service_search_06_query_misplaced_not_operator(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"- man _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert "Expected W:(abcd...)" in json_response["err"], "Actual Response : %r" % json_response

    def test_service_search_07_query_or_operator_within_parenthesis(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"(eagle OR man) _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 3, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 3, "Actual Response : %r" % json_response

    def test_service_search_08_query_and_operator(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"Iron AND man _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_09_query_parenthesis_only(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"(man) _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_10_query_parenthesis_only_multiple(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"(iron) _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 4, "Actual Response : %r" % json_response

    def test_service_search_11_query_or_not_operators_parenthesis(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"(iron OR eagle) -man _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 3, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 3, "Actual Response : %r" % json_response

    def test_service_search_12_query_misplaced_quote(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'"iron eagle -man _bucket:movies'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert "Expected \"\"\"" in json_response["err"], "Actual Response : %r" % json_response

    def test_service_search_13_query_field_operator(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"name:terminator _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_14_query_field_or_phrase_parenthesis_operators(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'(name:terminator) OR "star wars" _bucket:movies'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 2, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 2, "Actual Response : %r" % json_response

    def test_service_search_15_query_double_wildcard_operators(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"termin* or goon* _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 2, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 2, "Actual Response : %r" % json_response

    def test_service_search_16_wildcard_phrase_operators(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'ter* or "goonies" _bucket:movies'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 2, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 2, "Actual Response : %r" % json_response

    def test_service_search_17_multiple_field_operators(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"name:Harry or name:terminator _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 4, "Actual Response : %r" % json_response

    def test_service_search_18_ignore_stopwords_and_return_all(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"the _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 10, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 10, "Actual Response : %r" % json_response

    def test_service_search_19_ignore_stopwords(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"the matrix _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_20_add_new_stopwords(self):

        request = {"bucket":"_STOPWORDS", "key":"matrix"}
        response = self.app.post('/caching/add', data=json.dumps(request), content_type = 'application/json')

        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"the matrix _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 10, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 10, "Actual Response : %r" % json_response

    def test_service_search_21_remove_stopwords(self):

        request = {"bucket":"_STOPWORDS", "key":"matrix"}
        response = self.app.post('/caching/remove', data=json.dumps(request), content_type = 'application/json')

        # Build index with new stopword
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"the matrix _bucket:movies"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_23_max_results_and_pagination(self):

        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"harry _bucket:movies","num":1,"start":1}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_24_max_results_and_pagination(self):

        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"harry _bucket:movies","num":2,"start":2}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response

    def test_service_search_25_max_results_and_pagination(self):

        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"harry _bucket:movies","num":2,"start":1}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 2, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 2, "Actual Response : %r" % json_response

    def test_service_search_26_unicode_characters_index_and_search(self):

        self.run_before_service_searcher_tests_unicode()

        response = self.app.post('/service/search', data=json.dumps({"q":"Antonia's or Misérables or naïve or café _bucket:tests"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'_score': 1.0, u'_bucket': u'tests', u'_id': u'001', u'name': u"Antonia's"}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'002', u'name': u'Mis\xe9rables'}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'003', u'name': u'na\xefve'}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'004', u'name': u'caf\xe9'}], "Actual Response : %r" % json_response

    def test_service_search_27_unicode_characters_index_only(self):

        self.run_before_service_searcher_tests_unicode()

        response = self.app.post('/service/search', data=json.dumps({"q":"Antonia's or Miserables or naive or cafe _bucket:tests"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 4, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'_score': 1.0, u'_bucket': u'tests', u'_id': u'001', u'name': u"Antonia's"}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'002', u'name': u'Mis\xe9rables'}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'003', u'name': u'na\xefve'}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'004', u'name': u'caf\xe9'}], "Actual Response : %r" % json_response

    def test_service_search_28_unicode_characters_partial_query_stem_search(self):

        self.run_before_service_searcher_tests_unicode()


        response = self.app.post('/service/search', data=json.dumps({"q":"Antonia _bucket:tests"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["num_results"] == 1, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'_score': 1.0, u'_bucket': u'tests', u'_id': u'001', u'name': u"Antonia's"}], "Actual Response : %r" % json_response

    def test_service_search_29_multiple_term_originals(self):

        self.run_before_service_searcher_tests_multiple_originals()

        response = self.app.post('/service/search', data=json.dumps({"q":"Driving _bucket:tests"}), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'Driving _bucket:tests', u'documents': [{u'_score': 1.0, u'_bucket': u'tests', u'_id': u'005', u'name': u'Drive'}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'006', u'name': u'Driving'}, {u'_score': 1.0, u'_bucket': u'tests', u'_id': u'007', u'name': u'driving'}], u'num_results': 3}, "Actual Response : %r" % json_response

    def test_service_search_30_query_quote_with_stopwords_a(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'"Eagle Iron" _bucket:movies'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'"Eagle Iron" _bucket:movies', u'documents': [{u'_score': 1.0, u'_bucket': u'movies', u'_id': u'Eagle of Iron', u'name': u'Eagle of Iron'}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_31_query_quote_with_stopwords_b(self):
        self.run_before_service_searcher_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":'"Eagle of Iron" _bucket:movies'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'"Eagle of Iron" _bucket:movies', u'documents': [{u'_score': 1.0, u'_bucket': u'movies', u'_id': u'Eagle of Iron', u'name': u'Eagle of Iron'}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_32_query_all_bucket_documents(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"_bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 7, "Actual Response : %r" % json_response

    def test_service_search_33_query_numeric_operator_equal(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":'total:=250 _bucket:orders'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:=250 _bucket:orders', u'documents': [{u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.865009, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_34_query_numeric_operator_gt(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:>250 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:>250 _bucket:orders', u'documents': [{u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 1.633233, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}, {u'_id': u'004', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.320535, u'shipping': {u'city': u'san francisco', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/15/2015', u'total': 450}], u'num_results': 2}, "Actual Response : %r" % json_response

    def test_service_search_35_query_numeric_operator_get(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:>=300 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:>=300 _bucket:orders', u'documents': [{u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 1.633233, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}, {u'_id': u'004', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.320535, u'shipping': {u'city': u'san francisco', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/15/2015', u'total': 450}], u'num_results': 2}, "Actual Response : %r" % json_response

    def test_service_search_36_query_numeric_operator_lt(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:<250 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:<250 _bucket:orders', u'documents': [{u'_id': u'005', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 2.392164, u'shipping': {u'city': u'florida', u'state': u'fl'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 50}, {u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.432004, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 4}, "Actual Response : %r" % json_response

    def test_service_search_37_query_numeric_operator_let(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:<=250 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:<=250 _bucket:orders', u'documents': [{u'_id': u'005', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 2.392164, u'shipping': {u'city': u'florida', u'state': u'fl'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 50}, {u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.865009, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.432004, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 5}, "Actual Response : %r" % json_response

    def test_service_search_38_query_numeric_operator_all_inclusive_range(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:>=250&<=300 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:>=250&<=300 _bucket:orders', u'documents': [{u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.865009, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}, {u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 1.633233, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}], u'num_results': 2}, "Actual Response : %r" % json_response

    def test_service_search_39_query_numeric_operator_non_inclusive_range(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:>200&<300 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:>200&<300 _bucket:orders', u'documents': [{u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.865009, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_40a_query_nested_field_invalid_value(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"shipping.state:pa _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'shipping.state:pa _bucket:orders', u'documents': [], u'num_results': 0}, "Actual Response : %r" % json_response

    def test_service_search_40b_query_nested_field(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"shipping.state:ca _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'shipping.state:ca _bucket:orders', u'documents': [{u'total': 250, u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.290219, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'_id': u'001'}, {u'total': 300, u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 0.266435, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'_id': u'003'}, {u'total': 200, u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.243461, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'_id': u'002'}, {u'total': 450, u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.229199, u'shipping': {u'city': u'san francisco', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/15/2015', u'_id': u'004'}], u'num_results': 4}, "Actual Response : %r" % json_response

    def test_service_search_41_query_multiple_nested_fields(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"shipping.state:ca billing.city:florida _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'shipping.state:ca billing.city:florida _bucket:orders', u'documents': [{u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 0.376796, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_42_query_deep_nested_generic_field(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":".city:pittsburgh _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] ==  {u'query': u'.city:pittsburgh _bucket:orders', u'documents': [{u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.343752, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.288369, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'004', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.271476, u'shipping': {u'city': u'san francisco', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/15/2015', u'total': 450}], u'num_results': 3}, "Actual Response : %r" % json_response

    def test_service_search_43_query_deep_nested_generic_field_and_numeric_gt(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":".cost:>50 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.cost:>50 _bucket:orders', u'documents': [{u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 2}, "Actual Response : %r" % json_response

    def test_service_search_44_query_deep_nested_generic_field_and_numeric_range(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":".cost:>84.1&<84.9 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.cost:>84.1&<84.9 _bucket:orders', u'documents': [{u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 2}, "Actual Response : %r" % json_response

    def test_service_search_45_query_deep_nested_generic_field_with_quote(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":'.city:"los angeles" _bucket:orders'}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.city:"los angeles" _bucket:orders', u'documents': [{u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.486139, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}, {u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 0.446299, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 0.407815, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}], u'num_results': 3}, "Actual Response : %r" % json_response

    def test_service_search_46_query_date_greaterthan(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"order_date:>07/01/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'order_date:>07/01/2015 _bucket:orders', u'documents': [{u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 1.633233, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.432004, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 4}, "Actual Response : %r" % json_response

    def test_service_search_47_query_date_range(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"order_date:>07/01/2015&<11/01/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'order_date:>07/01/2015&<11/01/2015 _bucket:orders', u'documents': [{u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.432004, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 3}, "Actual Response : %r" % json_response

    def test_service_search_48_query_date_lessthan(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"order_date:<11/01/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'order_date:<11/01/2015 _bucket:orders', u'documents': [{u'_id': u'005', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 2.392164, u'shipping': {u'city': u'florida', u'state': u'fl'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 50}, {u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.865009, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.432004, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'004', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.320535, u'shipping': {u'city': u'san francisco', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/15/2015', u'total': 450}], u'num_results': 6}, "Actual Response : %r" % json_response

    def test_service_search_49_query_date_with_nested_field_format_1(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"shipping.shipping_date:Oct/02/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'shipping.shipping_date:Oct/02/2015 _bucket:orders', u'documents': [{u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_50_query_date_with_nested_field_format_2(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"shipping.shipping_date:=Oct/02/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'shipping.shipping_date:=Oct/02/2015 _bucket:orders', u'documents': [{u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_51_query_date_with_nested_field_format_3(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":".shipping_date:=Oct/02/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.shipping_date:=Oct/02/2015 _bucket:orders', u'documents': [{u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_52_query_date_range_with_nested_field(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":".shipping_date:>=Oct/02/2015&<=Oct/02/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.shipping_date:>=Oct/02/2015&<=Oct/02/2015 _bucket:orders', u'documents': [{u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_53_query_date_with_invalid_nested_field_should_return_nothing(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"shipping_date:=Oct/02/2015 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'shipping_date:=Oct/02/2015 _bucket:orders', u'documents': [], u'num_results': 0}, "Actual Response : %r" % json_response

    def test_service_search_54_query_numeric_operator_gt_negative(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:>-250 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:>-250 _bucket:orders', u'documents': [{u'_id': u'005', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 2.392164, u'shipping': {u'city': u'florida', u'state': u'fl'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 50}, {u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'001', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.865009, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 250}, {u'_id': u'003', u'billing': {u'city': u'florida', u'state': u'fl'}, u'_score': 1.633233, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Dec/01/2015', u'total': 300}, {u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.432004, u'shipping': {u'city': u'los angeles', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'004', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.320535, u'shipping': {u'city': u'san francisco', u'state': u'ca'}, u'_bucket': u'orders', u'order_date': u'Mar/15/2015', u'total': 450}], u'num_results': 7}, "Actual Response : %r" % json_response

    def test_service_search_55_query_numeric_operator_range_negative(self):
        self.run_before_service_searcher_tests_dates_numeric_and_deep_fields_operators()

        response = self.app.post('/service/search', data=json.dumps({"q":"total:>-250&<=50 _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'total:>-250&<=50 _bucket:orders', u'documents': [{u'_id': u'005', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 2.392164, u'shipping': {u'city': u'florida', u'state': u'fl'}, u'_bucket': u'orders', u'order_date': u'Mar/01/2015', u'total': 50}, {u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.871566, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}, {u'_id': u'007', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.335291, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipping_date': u'Oct/02/2015'}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 3}, "Actual Response : %r" % json_response

    def test_service_search_56_query_boolean_operator(self):
        self.run_before_service_searcher_tests_boolean_field_search()

        response = self.app.post('/service/search', data=json.dumps({"q":".shipped:=true _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.shipped:=true _bucket:orders', u'documents': [{u'_id': u'002', u'billing': {u'city': u'pittsburgh', u'state': u'pa'}, u'_score': 1.344435, u'shipping': {u'city': u'los angeles', u'state': u'ca', u'shipped': True}, u'_bucket': u'orders', u'order_date': u'Jul/12/2015', u'total': 200}], u'num_results': 1}, "Actual Response : %r" % json_response

    def test_service_search_57_query_boolean_operator(self):
        self.run_before_service_searcher_tests_boolean_field_search()

        response = self.app.post('/service/search', data=json.dumps({"q":".shipped:=false _bucket:orders"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == {u'query': u'.shipped:=false _bucket:orders', u'documents': [{u'_id': u'006', u'billing': {u'city': u'erie', u'state': u'pa'}, u'_score': 1.671488, u'shipping': {u'city': u'florida', u'state': u'fl', u'cost': 84.32, u'shipped': False}, u'_bucket': u'orders', u'order_date': u'Oct/01/2015', u'total': 50}], u'num_results': 1}, "Actual Response : %r" % json_response
