# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceClassifierTests(object):
    #
    # Service Classifier Tests
    #

    def run_before_service_classifier_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')
        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')
        response = self.app.post('/service/classifier/reset', data=json.dumps({}), content_type = 'application/json')

        # Adding Related Documents...

        request = {"documents":[{"_id":"001", "_bucket":"people", "name":"John"},{"_id":"002", "_bucket":"people", "name":"Peter"},{"_id":"003", "_bucket":"people", "name":"Thomas"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)

        taggings = {"documents":[{"_id":"article01", "_bucket":"articles","title":"What Google Sees In Augmented Reality", "source":"techcrunch"},{"_id":"article02", "_bucket":"articles","title":"Artificial Intelligence Nonprofit OpenAI Launches With Backing From Elon Musk And Sam Altman", "source":"techcrunch"},{"_id":"article03", "_bucket":"articles","title":"Can Tech Solve Climate Change?", "source":"techcrunch"},{"_id":"article04", "_bucket":"articles","title":"YouTube Gaming For Android Gets A “Cardboard Mode” For More Immersive Viewing", "source":"techcrunch"},{"_id":"article05", "_bucket":"articles","title":"House avoids government shutdown with hours to spare", "source":"cnn"}, {"_id":"article06", "_bucket":"articles","title":"Climate change deal the 'best chance' to save planet", "source":"cnn"},{"_id":"article07", "_bucket":"articles","title":"Elon Musk's next big thing", "source":"cnn"},{"_id":"article08", "_bucket":"articles","title":"Consensus on Need to Lower Global Carbon Emissions", "source":"nytimes"},{"_id":"article09", "_bucket":"articles","title":"What Does a Climate Deal Actually Mean for the World?", "source":"nytimes"},{"_id":"article10", "_bucket":"articles","title":"Climate Accord Is a Healing Step, if Not a Cure", "source":"nytimes"},{"_id":"article11", "_bucket":"articles","title":"Artificial-Intelligence Research Center Is Founded by Silicon Valley Investors", "source":"nytimes"}]}
        response = self.app.post('/document/put', data=json.dumps(taggings), content_type = 'application/json')
        json_response = json.loads(response.data)

        # Adding Actual Observations...

        observations = []
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article01", "value":["Tech","AI"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article02", "value":["AI","Innovation"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article03", "value":["Science"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article04", "value":["Gaming"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article05", "value":["Politics"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"002", "predicate":"tags", "object_id":"article06", "value":["Science"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"002", "predicate":"tags", "object_id":"article01", "value":["Technology"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"002", "predicate":"tags", "object_id":"article07", "value":["Artificial Intelligence"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article05", "value":["Politics"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article08", "value":["Global Warming","Politics"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article01", "value":["Google"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article01", "value":["Tech"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article04", "value":["Games"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article09", "value":["Science", "Politics"]})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"003", "predicate":"tags", "object_id":"article10", "value":"Science"})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"tags", "object_id":"article11", "value":"AI"})
        response = self.app.post('/observation/put', data=json.dumps(observations), content_type = 'application/json')
        json_response = json.loads(response.data)

        # Train Classification Model

        request = {"model":"tagged_articles", "subject_bucket":"people", "predicate":"tags"}
        response = self.app.post('/service/classifier/init', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        request = {"model":"tagged_articles", "features":["title","source"]}
        response = self.app.post('/service/classifier/train', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

    def run_before_service_classifier_tests_numbers_as_weights(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')
        response = self.app.post('/observation/reset', data=json.dumps({}), content_type = 'application/json')
        response = self.app.post('/service/classifier/reset', data=json.dumps({}), content_type = 'application/json')

        # Adding Related Documents...

        request = {"documents":[{"_id":"001", "_bucket":"people", "name":"John"},{"_id":"002", "_bucket":"people", "name":"Peter"},{"_id":"003", "_bucket":"people", "name":"Thomas"}]}
        response = self.app.post('/document/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)

        taggings = {"documents":[{"_id":"article01", "_bucket":"articles","title":"What Google Sees In Augmented Reality", "source":"techcrunch"},{"_id":"article02", "_bucket":"articles","title":"Artificial Intelligence Nonprofit OpenAI Launches With Backing From Elon Musk And Sam Altman", "source":"techcrunch"},{"_id":"article03", "_bucket":"articles","title":"Can Tech Solve Climate Change?", "source":"techcrunch"},{"_id":"article04", "_bucket":"articles","title":"YouTube Gaming For Android Gets A “Cardboard Mode” For More Immersive Viewing", "source":"techcrunch"},{"_id":"article05", "_bucket":"articles","title":"House avoids government shutdown with hours to spare", "source":"cnn"}, {"_id":"article06", "_bucket":"articles","title":"Climate change deal the 'best chance' to save planet", "source":"cnn"},{"_id":"article07", "_bucket":"articles","title":"Elon Musk's next big thing", "source":"cnn"},{"_id":"article08", "_bucket":"articles","title":"Consensus on Need to Lower Global Carbon Emissions", "source":"nytimes"},{"_id":"article09", "_bucket":"articles","title":"What Does a Climate Deal Actually Mean for the World?", "source":"nytimes"},{"_id":"article10", "_bucket":"articles","title":"Climate Accord Is a Healing Step, if Not a Cure", "source":"nytimes"},{"_id":"article11", "_bucket":"articles","title":"Artificial-Intelligence Research Center Is Founded by Silicon Valley Investors", "source":"nytimes"}]}
        response = self.app.post('/document/put', data=json.dumps(taggings), content_type = 'application/json')
        json_response = json.loads(response.data)

        # Adding Actual Observations...

        observations = []
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article01", "value":3})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article02", "value":3})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article03", "value":3})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article04", "value":3})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article05", "value":1})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"002", "predicate":"likes", "object_id":"article06", "value":3})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"002", "predicate":"likes", "object_id":"article01", "value":4})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"002", "predicate":"likes", "object_id":"article07", "value":4})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article05", "value":1})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article08", "value":1})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article01", "value":4})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article01", "value":5})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article04", "value":3})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article09", "value":1})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"003", "predicate":"likes", "object_id":"article10", "value":5})
        observations.append({"subject_bucket":"people", "object_bucket":"articles", "subject_id":"001", "predicate":"likes", "object_id":"article11", "value":3})
        response = self.app.post('/observation/put', data=json.dumps(observations), content_type = 'application/json')
        json_response = json.loads(response.data)

        # Train Classification Model - Using Numbers as Weights

        request = {"model":"liked_articles", "subject_bucket":"people", "predicate":"likes"}
        response = self.app.post('/service/classifier/init', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        request = {"model":"liked_articles", "features":["title","source"], "options":{"use_numbers_as_weights":True}}

        response = self.app.post('/service/classifier/train', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

    def test_service_classifier_01_invalid_or_unknown_subject_id(self):
        self.run_before_service_classifier_tests()

        request = {"model":"tagged_articles", "subject_id":"004", "document":{"title":"OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {'_score': None, '_ratio': None, 'label': None}, "Actual Response : %r" % json_response

    def test_service_classifier_02_best_classification_for_document__single_label_scenario(self):
        self.run_before_service_classifier_tests()

        request = {"model":"tagged_articles", "subject_id":"003", "document":{"title":"OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] ==  {'label': 'Science', '_score': 1.0, '_ratio': 100.0}, "Actual Response : %r" % json_response

    def test_service_classifier_03_best_classification_for_document__multiple_labels_scenario(self):
        self.run_before_service_classifier_tests()

        request = {"model":"tagged_articles", "subject_id":"001", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {u'_score': 26.426909, u'_ratio': 81.469171, u'label': u'AI'}, "Actual Response : %r" % json_response

    def test_service_classifier_04_label_classification_for_document(self):
        self.run_before_service_classifier_tests()

        request = {"model":"tagged_articles", "subject_id":"001", "label":"Innovation", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {u'_score': 4.774199, u'_ratio': 14.717953, u'label': u'Innovation'}, "Actual Response : %r" % json_response

    def test_service_classifier_05_all_prediction_scores_for_document(self):
        self.run_before_service_classifier_tests()

        request = {"model":"tagged_articles", "subject_id":"001", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predictions', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == [{u'_score': 26.426909, u'_ratio': 81.469171, u'label': u'AI'}, {u'_score': 4.774199, u'_ratio': 14.717953, u'label': u'Innovation'}, {u'_score': 0.440237, u'_ratio': 1.357167, u'label': u'Tech'}, {u'_score': 0.2, u'_ratio': 0.616562, u'label': u'Politics'}, {u'_score': 0.158974, u'_ratio': 0.490088, u'label': u'Google'}, {u'_score': 0.158974, u'_ratio': 0.490088, u'label': u'Science'}, {u'_score': 0.105983, u'_ratio': 0.326725, u'label': u'Gaming'}, {u'_score': 0.105983, u'_ratio': 0.326725, u'label': u'Games'}, {u'_score': 0.066667, u'_ratio': 0.205521, u'label': u'Global Warming'}], "Actual Response : %r" % json_response

    def test_service_classifier_06_nothing_returns_from_empty_model(self):
        self.run_before_service_classifier_tests()

        request = {"model":"tagged_articles"}
        response = self.app.post('/service/classifier/clear', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        request = {"model":"tagged_articles", "subject_id":"001", "label":"Innovation", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {'label': None, '_score': None, '_ratio': None}, "Actual Response : %r" % json_response

    def test_service_classifier_07_best_classification_for_document__single_label_scenario__naw(self):
        self.run_before_service_classifier_tests_numbers_as_weights()

        request = {"model":"liked_articles", "subject_id":"003", "document":{"title":"OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] ==  {u'_score': 1.0, u'_ratio': 100.0, u'label': u'5'}, "Actual Response : %r" % json_response

    def test_service_classifier_08_best_classification_for_document__multiple_labels_scenario__naw(self):
        self.run_before_service_classifier_tests_numbers_as_weights()

        request = {"model":"liked_articles", "subject_id":"001", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {u'_score': 60.641218, u'_ratio': 99.477004, u'label': u'3'}, "Actual Response : %r" % json_response

    def test_service_classifier_09_label_classification_for_document__naw(self):
        self.run_before_service_classifier_tests_numbers_as_weights()

        request = {"model":"liked_articles", "subject_id":"001", "label":"5", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {u'_score': 0.076076, u'_ratio': 0.124797, u'label': u'5'}, "Actual Response : %r" % json_response

    def test_service_classifier_10_all_prediction_scores_for_document__naw(self):
        self.run_before_service_classifier_tests_numbers_as_weights()

        request = {"model":"liked_articles", "subject_id":"001", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predictions', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == [{u'_score': 60.641218, u'_ratio': 99.477004, u'label': u'3'}, {u'_score': 0.166667, u'_ratio': 0.273403, u'label': u'1'}, {u'_score': 0.076076, u'_ratio': 0.124797, u'label': u'5'}, {u'_score': 0.076076, u'_ratio': 0.124797, u'label': u'4'}], "Actual Response : %r" % json_response

    def test_service_classifier_11_nothing_returns_from_empty_model__naw(self):
        self.run_before_service_classifier_tests_numbers_as_weights()

        request = {"model":"liked_articles"}
        response = self.app.post('/service/classifier/clear', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        request = {"model":"liked_articles", "subject_id":"001", "label":"Innovation", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}}
        response = self.app.post('/service/classifier/predict', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["result"] == {'label': None, '_score': None, '_ratio': None}, "Actual Response : %r" % json_response
