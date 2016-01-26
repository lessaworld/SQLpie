# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceMatchingTests(object):
    #
    # Service Matching Tests
    #

    def run_before_service_matching_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')
        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')

        request = {"documents":[{"_id":"c001", "_bucket":"candidates", "name":"John", "resume":"Software Engineer with 5 years of Python experience."},{"_id":"c002", "_bucket":"candidates", "name":"Peter", "resume":"Marketing and Social media Specialist. Experience creating website designs and monitoring social media activities."},{"_id":"c003", "_bucket":"candidates", "name":"Thomas", "resume":"Experienced Software Engineer with over 10 years of experience creating web applications, primarily in Java Swing."}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')

        request = {"documents":[{"_id":"j001", "_bucket":"jobs", "name":"Software Engineer", "state":"pa", "description":"python engineer with experience developing web applications."},{"_id":"j002", "_bucket":"jobs", "name":"Web Developer", "state":"ny", "description":"experience creating web applications using ruby on rails and javascript JQuery."},{"_id":"j003", "_bucket":"jobs", "name":"Senior Software Engineer", "state":"pa", "description":"software engineer with experience developing web applications. Python, Ruby, and R experience required."},{"_id":"j004", "_bucket":"jobs", "name":"Social Media Specialist", "state":"ca", "description":"monitor twitter and facebook feeds and keep track of Google Analytics"},{"_id":"j005", "_bucket":"jobs", "name":"Java Developer", "state":"ca", "description":"experience building web applications using Java Swing and deploying code to Tomcat Application Servers."}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')

        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def test_service_matching_01_single_document_top_match(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "document_id":"c003", "search_bucket":"jobs"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == [{u'description': u'experience building web applications using Java Swing and deploying code to Tomcat Application Servers.', u'state': u'ca', u'_bucket': u'jobs', u'_score': 0.708955, u'_id': u'j005', u'name': u'Java Developer'}], "Actual Response : %r" % json_response

    def test_service_matching_02_single_document_multiple_matches(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "document_id":"c003", "search_bucket":"jobs", "num_results":5}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == [{u'description': u'experience building web applications using Java Swing and deploying code to Tomcat Application Servers.', u'state': u'ca', u'_bucket': u'jobs', u'_score': 0.708955, u'_id': u'j005', u'name': u'Java Developer'}, {u'description': u'software engineer with experience developing web applications. Python, Ruby, and R experience required.', u'state': u'pa', u'_bucket': u'jobs', u'_score': 0.587714, u'_id': u'j003', u'name': u'Senior Software Engineer'}, {u'description': u'python engineer with experience developing web applications.', u'state': u'pa', u'_bucket': u'jobs', u'_score': 0.571081, u'_id': u'j001', u'name': u'Software Engineer'}, {u'description': u'experience creating web applications using ruby on rails and javascript JQuery.', u'state': u'ny', u'_bucket': u'jobs', u'_score': 0.566924, u'_id': u'j002', u'name': u'Web Developer'}], "Actual Response : %r" % json_response

    def test_service_matching_03_single_document_filtered_matches(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "document_id":"c003", "search_bucket":"jobs", "filter_query":"state:PA"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == [{'description': 'software engineer with experience developing web applications. Python, Ruby, and R experience required.', '_bucket': 'jobs', 'state': 'pa', '_score': 0.587714, '_id': 'j003', 'name': 'Senior Software Engineer'}], "Actual Response : %r" % json_response

    def test_service_matching_04_all_documents_multiple_matches(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "search_bucket":"jobs", "num_results":5}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["total_matches"] == 13, "Actual Response : %r" % json_response
        assert json_response["output_predicate"] == "match_candidates_jobs", "Actual Response : %r" % json_response

        observation = {"predicate":"match_candidates_jobs"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

    def test_service_matching_05_all_documents_multiple_matches_custom_output_predicate(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "search_bucket":"jobs", "num_results":5, "output_predicate":"monthly_report"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["total_matches"] == 13, "Actual Response : %r" % json_response
        assert json_response["output_predicate"] == "monthly_report", "Actual Response : %r" % json_response

        observation = {"predicate":"monthly_report"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

    def test_service_matching_06_all_documents_and_query_filter(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "search_bucket":"jobs", "filter_query":"state:PA ruby"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["total_matches"] ==3, "Actual Response : %r" % json_response
        assert json_response["output_predicate"] == "match_candidates_jobs", "Actual Response : %r" % json_response

        observation = {"predicate":"match_candidates_jobs"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 3, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 3, "Actual Response : %r" % json_response

    def test_service_matching_07_all_documents_and_query_filter_no_results(self):
        self.run_before_service_matching_tests()

        request = {"bucket":"candidates", "search_bucket":"jobs", "filter_query":"state:PA java"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["total_matches"] == 0, "Actual Response : %r" % json_response
        assert json_response["output_predicate"] == "match_candidates_jobs", "Actual Response : %r" % json_response

        observation = {"predicate":"match_candidates_jobs"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 0, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 0, "Actual Response : %r" % json_response

    def test_service_matching_08_new_document(self):
        self.run_before_service_matching_tests()

        request = {"document":{"name":"John", "resume":"Software Engineer with 5 years of Python experience."}, "search_bucket":"jobs"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == [{u'description': u'software engineer with experience developing web applications. Python, Ruby, and R experience required.', u'state': u'pa', u'_bucket': u'jobs', u'_score': 0.247016, u'_id': u'j003', u'name': u'Senior Software Engineer'}], "Actual Response : %r" % json_response


    def test_service_matching_09_new_document_and_query_filter(self):
        self.run_before_service_matching_tests()

        request = {"document":{"name":"John", "resume":"Software Engineer with 5 years of Python experience."}, "search_bucket":"jobs", "filter_query":"state:PA"}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == [{u'description': u'software engineer with experience developing web applications. Python, Ruby, and R experience required.', u'state': u'pa', u'_bucket': u'jobs', u'_score': 0.247016, u'_id': u'j003', u'name': u'Senior Software Engineer'}], "Actual Response : %r" % json_response

    def test_service_matching_10_new_document_and_query_filter_multiple_matches(self):
        self.run_before_service_matching_tests()

        request = {"document":{"name":"John", "resume":"Software Engineer with 5 years of Python or Ruby experience."}, "search_bucket":"jobs", "filter_query":"state:PA", "num_results":3}
        response = self.app.post('/service/matching/', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"] == [{u'description': u'software engineer with experience developing web applications. Python, Ruby, and R experience required.', u'state': u'pa', u'_bucket': u'jobs', u'_score': 0.27677, u'_id': u'j003', u'name': u'Senior Software Engineer'}, {u'description': u'python engineer with experience developing web applications.', u'state': u'pa', u'_bucket': u'jobs', u'_score': 0.241152, u'_id': u'j001', u'name': u'Software Engineer'}], "Actual Response : %r" % json_response

