# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie
import math, json

class Classifier(object):

    USE_NUMBERS_AS_WEIGHTS_PARAM = "use_numbers_as_weights"

    def __init__(self, model, subject_bucket=None, predicate=None):
        self.model = model.strip()
        self.subject_bucket = subject_bucket.strip()
        self.predicate = predicate.strip()
        self.model_id = sqlpie.Util.to_sha1(self.model)
        self.subject_bucket_id = sqlpie.Util.to_sha1(subject_bucket)
        self.predicate_id = sqlpie.Util.to_sha1(predicate)
        m = sqlpie.Model().create(self.model, self.subject_bucket, self.predicate, \
            self.model_id, self.subject_bucket_id, self.predicate_id)

    @staticmethod
    def train(model, relevant_features=[], use_numbers_as_weights=False):
        model_id = sqlpie.Util.to_sha1(model.strip())
        m = sqlpie.Model().get(model_id)
        query = {"subject_bucket":m.subject_bucket, "predicate":m.predicate, \
                    "timestamp":{"start":m.last_observation}, "options":{"limit":1000, "offset":0}}
        observations, total = sqlpie.Observation.get(query)

        mc = sqlpie.ModelClassifier(m.model_id)
        for o in observations:
            subject_id = sqlpie.Util.to_sha1(o["subject_id"].strip())
            if sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_LIST:
                for value in o["value"]:
                    label = unicode(value)
                    mc.increment_label(subject_id, label)
            elif sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_UNICODE:
                label = o["value"]
                mc.increment_label(subject_id, label)
            else:
                label = json.dumps(o["value"])
                incr = 1
                if use_numbers_as_weights and (sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_FLOAT or \
                    sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_INT):
                    weight = o["value"]
                    incr = incr * weight
                mc.increment_label(subject_id, label, incr)

            bucket_id = sqlpie.Util.to_sha1(o["object_bucket"])
            document_id = sqlpie.Util.to_sha1(o["object_id"])
            doc = sqlpie.Document.get(bucket_id, document_id)

            features = sqlpie.Indexer.parse_features(doc.document, relevant_features)
            counts = Classifier._count_words(features)
            for feature, incr in list(counts.items()):
                if use_numbers_as_weights and (sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_FLOAT or \
                    sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_INT):
                    weight = o["value"]
                    incr = incr * weight
                mc.increment_feature(subject_id, feature, incr)
                if sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_LIST:
                    for value in o["value"]:
                        label = unicode(value)
                        mc.increment_label_feature(subject_id, label, feature, incr)
                elif sqlpie.Predicate.convert_type(o["value"]) == sqlpie.Predicate.IS_UNICODE:
                    label = o["value"]
                    mc.increment_label_feature(subject_id, label, feature, incr)
                else:
                    label = json.dumps(o["value"])
                    mc.increment_label_feature(subject_id, label, feature, incr)

    @staticmethod
    def clear(model):
        model_id = sqlpie.Util.to_sha1(model.strip())
        mc = sqlpie.ModelClassifier(model_id)
        mc.clear()

    @staticmethod
    def predict(model, subject, document, label_param=None, best_prediction_only=True):
        model_id = sqlpie.Util.to_sha1(model.strip())
        subject_id = sqlpie.Util.to_sha1(subject.strip())

        mc = sqlpie.ModelClassifier(model_id)

        features = sqlpie.Indexer.parse_features(document)
        counts = Classifier._count_words(features)

        target_labels = mc.get_labels(subject_id)
        sum_all_labels = sum(target_labels.values())
        sum_all_features = mc.sum_all_features(subject_id)
        doc_features = mc.get_document_features(subject_id, features)
        total, label_param_score, label_param_ratio = 0.0, 0.0, 0.0
        scores = {}

        for label in target_labels:
            if sum_all_labels == 0:
                prior_label = 0.0
            else:
                prior_label = target_labels[label] / sum_all_labels
            log_prob_label = 0.0

            sum_feature_values = mc.sum_feature_values(subject_id, label)
            label_features = mc.get_label_features(subject_id, label, counts.keys())

            for w, cnt in list(counts.items()):
                if sum_all_features == 0 or w not in doc_features:
                    p_word = 0.0
                else:
                    p_word = doc_features[w] / sum_all_features

                if sum_feature_values == 0 or w not in label_features:
                    p_w_given_label = 0.0
                else:
                    p_w_given_label = label_features[w] / sum_feature_values

                if p_w_given_label > 0 and p_word > 0:
                    log_prob_label += math.log(cnt * p_w_given_label / p_word)

            score_label =  math.exp(log_prob_label + math.log(prior_label))
            total += score_label
            scores[label] = score_label

        for k, v in scores.iteritems():
            score_label = float("{0:.6f}".format(v))
            if total == 0:
                ratio_label = 0.0
            else:
                ratio_label = float("{0:.6f}".format((v/total) * 100))
            scores[k] = {'label':k, '_score':score_label, '_ratio':ratio_label}
            if k == label_param:
                label_param_score, label_param_ratio = score_label, ratio_label

        scores = [k[1] for k in sorted(scores.items(), key=lambda (k,v): -v["_score"])]

        if best_prediction_only:
            if len(scores) > 0 and label_param is None:
                response = scores[0]
            elif len(scores) > 0 and label_param is not None:
                response = {'label':label_param, '_score':label_param_score, '_ratio':label_param_ratio}
            else:
                response = {'label':None, '_score':None, '_ratio':None}
        else:
            if label_param is not None:
                response = {'label':label_param, '_score':label_param_score, '_ratio':label_param_ratio}
            else:
                response = scores
        return response

    #
    # private
    #

    @staticmethod
    def _count_words(words):
        wc = {}
        for word in words:
            wc[word] = wc.get(word, 0.0) + 1.0
        return wc
