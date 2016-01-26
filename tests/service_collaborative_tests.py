# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceCollaborativeTests(object):
    #
    # Service Recommendation Tests
    #

    def run_before_service_recommendation_tests(self):
        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')

        observation = []
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"001", "predicate":"likes", "object_id":"Java Engineer", "value":3, "timestamp":972654989})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"001", "predicate":"likes", "object_id":"Java Software Engineer", "value":5, "timestamp":972654989})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"001", "predicate":"likes", "object_id":"Software Engineer", "value":4, "timestamp":972654989})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"001", "predicate":"likes", "object_id":"Senior Java Engineer", "value":2.5, "timestamp":972654989})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"001", "predicate":"likes", "object_id":"Java Software Engineer", "value":0, "timestamp":972654989})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"002", "predicate":"likes", "object_id":"MySQL DBA", "value":4, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"002", "predicate":"likes", "object_id":"Data Scientist", "value":2, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"002", "predicate":"likes", "object_id":"Oracle DBA", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"003", "predicate":"likes", "object_id":"Java Software Engineer", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"003", "predicate":"likes", "object_id":"Python Engineer", "value":3, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"003", "predicate":"likes", "object_id":"Java Engineer", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"003", "predicate":"likes", "object_id":"Senior Java Engineer", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"003", "predicate":"likes", "object_id":"Java Software Engineer", "value":2.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"004", "predicate":"likes", "object_id":"Oracle DBA", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"004", "predicate":"likes", "object_id":"MySQL DBA", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"005", "predicate":"likes", "object_id":"Data Scientist", "value":3.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"005", "predicate":"likes", "object_id":"MySQL DBA", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"006", "predicate":"likes", "object_id":"Oracle DBA", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"006", "predicate":"likes", "object_id":"MySQL DBA", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"006", "predicate":"likes", "object_id":"Data Scientist", "value":3, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"007", "predicate":"likes", "object_id":"MySQL SysAdmin", "value":4, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"007", "predicate":"likes", "object_id":"MySQL DBA", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"008", "predicate":"likes", "object_id":"MySQL SysAdmin", "value":3.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"008", "predicate":"likes", "object_id":"Oracle DBA", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"009", "predicate":"likes", "object_id":"Java Engineer II", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"candidates", "object_bucket":"jobs", "subject_id":"009", "predicate":"likes", "object_id":"Senior Java Engineer", "value":4.5, "timestamp":1445954189})

        response = self.app.post('/observation/put', data=json.dumps(observation), content_type = 'application/json')

    def test_service_collaborative_01_similarity_subject_pearson(self):
        self.run_before_service_recommendation_tests()

        #
        # subject_ids that are similar to this subject_id in terms of "liking" these "objects"
        #

        request = {"subject_bucket":"candidates", "subject_id":"001", "predicate":"likes", "object_bucket":"jobs", "method":"pearson"}
        response = self.app.post('/service/collaborative/similarity', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{u'bucket_id': u'candidates', u'num': 6, u'_score': 0.03288, u'document_id': u'003'}, {u'bucket_id': u'candidates', u'num': 1, u'_score': 0.0, u'document_id': u'009'}], "Actual Response : %r" % json_response

    def test_service_collaborative_02_similarity_object_pearson(self):
        self.run_before_service_recommendation_tests()

        #
        # object_ids that are similar to this object_id in terms of being "liked" by these "subjects"
        #

        request = {"subject_bucket":"candidates", "predicate":"likes", "object_bucket":"jobs", "object_id":"MySQL DBA", "method":"pearson"}
        response = self.app.post('/service/collaborative/similarity', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{u'bucket_id': u'jobs', u'num': 3, u'_score': 0.944911, u'document_id': u'Data Scientist'}, {u'bucket_id': u'jobs', u'num': 3, u'_score': 0.0, u'document_id': u'Oracle DBA'}, {u'bucket_id': u'jobs', u'num': 1, u'_score': 0.0, u'document_id': u'MySQL SysAdmin'}], "Actual Response : %r" % json_response

    def test_service_collaborative_03_similarity_subject_manhattan(self):
        self.run_before_service_recommendation_tests()

        #
        # subject_ids that are similar to this subject_id in terms of "liking" these "objects"
        #

        request = {"subject_bucket":"candidates", "subject_id":"001", "predicate":"likes", "object_bucket":"jobs", "method":"manhattan"}
        response = self.app.post('/service/collaborative/similarity', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{u'bucket_id': u'candidates', u'num': 6, u'_score': 0.03288, u'document_id': u'003'}, {u'bucket_id': u'candidates', u'num': 1, u'_score': 0.0, u'document_id': u'009'}], "Actual Response : %r" % json_response

    def test_service_collaborative_04_similarity_object_manhattan(self):
        self.run_before_service_recommendation_tests()

        #
        # object_ids that are similar to this object_id in terms of being "liked" by these "subjects"
        #

        request = {"subject_bucket":"candidates", "predicate":"likes", "object_bucket":"jobs", "object_id":"MySQL DBA", "method":"manhattan"}
        response = self.app.post('/service/collaborative/similarity', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{u'bucket_id': u'jobs', u'num': 3, u'_score': 0.944911, u'document_id': u'Data Scientist'}, {u'bucket_id': u'jobs', u'num': 3, u'_score': 0.0, u'document_id': u'Oracle DBA'}, {u'bucket_id': u'jobs', u'num': 1, u'_score': 0.0, u'document_id': u'MySQL SysAdmin'}], "Actual Response : %r" % json_response

    def test_service_collaborative_05_recommendation_pearson_object_for_subject(self):
        self.run_before_service_recommendation_tests()

        #
        # based on object_ids "liked" by all subject_ids, what object_id should be recommended for this subject_id next
        #

        request = {"subject_bucket":"candidates", "subject_id":"001", "predicate":"likes", "object_bucket":"jobs"}
        response = self.app.post('/service/collaborative/recommendation', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{'bucket_id': 'jobs', '_score': 3.0, 'document_id': 'Python Engineer'}, {'bucket_id': 'jobs', '_score': 0.0, 'document_id': 'Java Engineer II'}], "Actual Response : %r" % json_response

    def test_service_collaborative_06_recommendation_manhattan_object_for_subject(self):
        self.run_before_service_recommendation_tests()

        #
        # based on object_ids "liked" by all subject_ids, what object_id should be recommended for this subject_id next
        #

        request = {"subject_bucket":"candidates", "subject_id":"001", "predicate":"likes", "object_bucket":"jobs", "metric":"manhattan"}
        response = self.app.post('/service/collaborative/recommendation', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{u'bucket_id': u'jobs', u'_score': 2.076923, u'document_id': u'Java Engineer II'}, {u'bucket_id': u'jobs', u'_score': 1.615385, u'document_id': u'Python Engineer'}], "Actual Response : %r" % json_response

    def test_service_collaborative_07_recommendation_pearson_subject_for_object(self):
        self.run_before_service_recommendation_tests()

        #
        # based on subject_ids "who liked" these object_ids, what subject_id should be recommended for this object_id next
        #

        request = {"subject_bucket":"candidates", "predicate":"likes", "object_bucket":"jobs", "object_id":"Java Software Engineer"}
        response = self.app.post('/service/collaborative/recommendation', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{'bucket_id': 'candidates', '_score': 2.25, 'document_id': '009'}], "Actual Response : %r" % json_response

    def test_service_collaborative_08_recommendation_manhattan_subject_for_object(self):
        self.run_before_service_recommendation_tests()

        #
        # based on subject_ids "who liked" these object_ids, what subject_id should be recommended for this object_id next
        #

        request = {"subject_bucket":"candidates", "predicate":"likes", "object_bucket":"jobs", "object_id":"Java Software Engineer", "metric":"manhattan"}
        response = self.app.post('/service/collaborative/recommendation', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["results"] == [{'bucket_id': 'candidates', '_score': 1.125, 'document_id': '009'}], "Actual Response : %r" % json_response

