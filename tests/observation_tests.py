# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ObservationTests(object):

    #
    # Observation Tests
    #

    def run_before_observation_tests(self):

        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')

        observation = []
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod001", "value":3, "timestamp":972654989})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod002", "value":5, "timestamp":972654989})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod003", "value":4, "timestamp":972654989})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod004", "value":2.5, "timestamp":972654989})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod005", "value":0, "timestamp":972654989})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"002", "predicate":"likes", "object_id":"Prod006", "value":4, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"002", "predicate":"likes", "object_id":"Prod001", "value":2, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"002", "predicate":"likes", "object_id":"Prod007", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod005", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod008", "value":3, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod001", "value":5, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod004", "value":4.5, "timestamp":1445954189})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod005", "value":2.5, "timestamp":1445954189})
        response = self.app.post('/observation/put', data=json.dumps(observation), content_type = 'application/json')

    def test_observation_put(self):
        #
        # Adding Related (Multiple Documents....
        #
        request = {"documents":[{"_id":"001", "_bucket":"customers", "name":"John"},{"_id":"002", "_bucket":"customers", "name":"Peter"},{"_id":"003", "_bucket":"customers", "name":"Thomas"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 3, "Actual Response : %r" % json_response

        books = {"documents":[{"_id":"Prod001", "_bucket":"products","name":"Prod001"},{"_id":"Prod002", "_bucket":"products","name":"Prod002"},{"_id":"Prod003", "_bucket":"products","name":"Prod003"},{"_id":"Prod004", "_bucket":"products","name":"Prod004"},{"_id":"Prod005", "_bucket":"products","name":"Prod005"}, {"_id":"Prod006", "_bucket":"products","name":"Prod006"},{"_id":"Prod007", "_bucket":"products","name":"Prod007"},{"_id":"Prod008", "_bucket":"products","name":"Prod008"},{"_id":"Prod009", "_bucket":"products","name":"Prod009"},{"_id":"Prod010", "_bucket":"products","name":"Prod010"},{"_id":"Prod011", "_bucket":"products","name":"Prod011"}]}
        response = self.app.post('/document/put', data=json.dumps(books), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 11, "Actual Response : %r" % json_response

        #
        # Adding Actual Observations
        #
        observation = []
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod001", "value":3})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod002", "value":5})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod003", "value":4})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod004", "value":2.5})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod005", "value":0})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"002", "predicate":"likes", "object_id":"Prod006", "value":4})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"002", "predicate":"likes", "object_id":"Prod001", "value":2})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"002", "predicate":"likes", "object_id":"Prod007", "value":5})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod005", "value":5})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod008", "value":3})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod001", "value":5})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod004", "value":4.5})
        observation.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"003", "predicate":"likes", "object_id":"Prod005", "value":2.5})
        response = self.app.post('/observation/put', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 13, "Actual Response : %r" % json_response

    def test_observation_reset(self):
        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

    def test_observation_get_success(self):
        #
        # Prepare Observations Data
        #
        self.run_before_observation_tests()

        observation = {"subject_bucket":"customers"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":"001"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 5, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":["001","002"]}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 8, "Actual Response : %r" % json_response

        observation = {"predicate":"likes"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

        observation = {"predicate":["likes"]}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":"001", "value":{"start":3, "end":5}}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 3, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":"001", "timestamp":{"start":972654980, "end":972655000}}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 5, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "options":{"limit":10, "offset":0}}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "options":{"limit":10, "offset":10}}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 3, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":"001", "options":{"limit":5}}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 5, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 5, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":"001", "options":{"offset":4}}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 1, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 5, "Actual Response : %r" % json_response

    def test_observation_get_fail(self):
        #
        # Prepare Observations Data
        #
        self.run_before_observation_tests()

        observation = {"subject_bucket":"customers", "subject_id":"001z"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 0, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 0, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers0"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 0, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 0, "Actual Response : %r" % json_response

        observation = {"subject_bucket":["customers0"]}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True
        assert json_response["record_count"] == 0, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 0, "Actual Response : %r" % json_response

    def test_observation_remove_success(self):
        #
        # Prepare Observations Data
        #
        self.run_before_observation_tests()

        observation = {"subject_bucket":"customers", "subject_id":"001"}
        response = self.app.post('/observation/remove', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 5, "Actual Response : %r" % json_response

        # Confirm the deletion happened
        observation = {"subject_bucket":"customers"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 8, "Actual Response : %r" % json_response

    def test_observation_remove_fail(self):
        #
        # Prepare Observations Data
        #
        self.run_before_observation_tests()

        observation = {"subject_bucket":"customers"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

        observation = {"subject_bucket":"customers", "subject_id":"002z"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 0, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 0, "Actual Response : %r" % json_response

        # Confirm the deletion NOT happened

        observation = {"subject_bucket":"customers"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 10, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 13, "Actual Response : %r" % json_response

    def test_observation_predicate_types(self):
        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')

        observation = []
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":3})
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document002", "value":5.34})
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document003", "value":True})
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document004", "value":["Action","Drama"]})
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document005", "value":None})
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document006", "value":"Very Good"})
        observation.append({"subject_bucket":"people", "object_bucket":"documents", "subject_id":"001", "predicate":"likes", "object_id":"Document007", "value":{"expired":True}})

        response = self.app.post('/observation/put', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 7, "Actual Response : %r" % json_response

        observation = {"predicate":"likes"}
        response = self.app.post('/observation/get', data=json.dumps(observation), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["record_count"] == 7, "Actual Response : %r" % json_response
        assert json_response["total_count"] == 7, "Actual Response : %r" % json_response
        assert json_response["observations"] == [{'predicate': 'likes', 'subject_id': '001', 'value': 3, 'subject_bucket': 'people', 'object_id': 'Document001', 'object_bucket': 'documents'}, {'predicate': 'likes', 'subject_id': '001', 'value': 5.34, 'subject_bucket': 'people', 'object_id': 'Document002', 'object_bucket': 'documents'}, {'predicate': 'likes', 'subject_id': '001', 'value': True, 'subject_bucket': 'people', 'object_id': 'Document003', 'object_bucket': 'documents'}, {'predicate': 'likes', 'subject_id': '001', 'value': ['Action', 'Drama'], 'subject_bucket': 'people', 'object_id': 'Document004', 'object_bucket': 'documents'}, {'predicate': 'likes', 'subject_id': '001', 'value': None, 'subject_bucket': 'people', 'object_id': 'Document005', 'object_bucket': 'documents'}, {'predicate': 'likes', 'subject_id': '001', 'value': 'Very Good', 'subject_bucket': 'people', 'object_id': 'Document006', 'object_bucket': 'documents'}, {'predicate': 'likes', 'subject_id': '001', 'value': {'expired': True}, 'subject_bucket': 'people', 'object_id': 'Document007', 'object_bucket': 'documents'}]


        