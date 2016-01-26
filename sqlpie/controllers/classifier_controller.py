# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Response
import json
import sqlpie

class ClassifierController(sqlpie.BaseController):

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def classifier_init(request=None):
        json_data = request.get_json()
        if (not "model" in json_data) or (not "subject_bucket" in json_data) or (not "predicate" in json_data):
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        model = json_data["model"]
        subject_bucket = json_data["subject_bucket"]
        predicate = json_data["predicate"]
        if len(model.strip()) == 0 or len(subject_bucket.strip()) == 0 or len(predicate.strip()) == 0:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        sqlpie.Classifier(model, subject_bucket, predicate)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def classifier_train(request=None):
        json_data = request.get_json()
        if not "model" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "features" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)

        use_numbers_as_weights = False
        if "options" in json_data:
            options = json_data["options"]
            if sqlpie.Classifier.USE_NUMBERS_AS_WEIGHTS_PARAM in options:
                use_numbers_as_weights = options[sqlpie.Classifier.USE_NUMBERS_AS_WEIGHTS_PARAM]

        model = json_data["model"]
        features = json_data["features"]
        if len(model.strip()) == 0:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        sqlpie.Classifier.train(model, features, use_numbers_as_weights)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def classifier_clear(request=None):
        json_data = request.get_json()
        if not "model" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        model = json_data["model"]
        if len(model.strip()) == 0:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        sqlpie.Classifier.clear(model)
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def classifier_reset(request=None):
        sqlpie.Model.reset()
        sqlpie.ModelClassifier.reset()
        return {'success': True}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def classifier_predict(request=None):
        json_data = request.get_json()
        if not "model" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "subject_id" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "document" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        model = json_data["model"]
        subject_id = json_data["subject_id"]
        document = json_data["document"]
        if len(model.strip()) == 0 or len(subject_id.strip()) == 0 or (type(document) is not dict):
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if "label" in json_data:
            label = json_data["label"]
        else:
            label = None
        best_prediction_only = True
        prediction = sqlpie.Classifier.predict(model, subject_id, document, label, best_prediction_only)
        return {'success': True, 'result':prediction}

    @staticmethod
    @sqlpie.BaseController.controller_wrapper
    def classifier_predictions(request=None):
        json_data = request.get_json()
        if not "model" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "subject_id" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        if not "document" in json_data:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        model = json_data["model"]
        subject_id = json_data["subject_id"]
        document = json_data["document"]
        if len(model.strip()) == 0 or len(subject_id.strip()) == 0 or (type(document) is not dict):
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        label, best_prediction_only = None, False
        predictions = sqlpie.Classifier.predict(model, subject_id, document, label, best_prediction_only)
        return {'success': True, 'result':predictions}
