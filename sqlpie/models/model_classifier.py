# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class ModelClassifier(object):
    __tablename = "model_classifiers"
    LABEL_TYPE = 0
    FEATURE_TYPE = 1
    LABEL_FEATURE_TYPE = 2
    NULL_MAGIC_VALUE = "nil"

    def __init__(self, model_id):
        self.model_id = model_id

    def increment_label(self, subject_id, label, incr=1):
        sql = "INSERT INTO " + self.__tablename
        sql += " (model_id, subject_id, score_type, label, feature) VALUES (UNHEX(%s), UNHEX(%s), %s, %s, %s)"
        sql += " ON DUPLICATE KEY UPDATE score = score + %s"
        g.cursor.execute(sql, (self.model_id, subject_id, ModelClassifier.LABEL_TYPE, label, ModelClassifier.NULL_MAGIC_VALUE, incr))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def increment_feature(self, subject_id, feature, incr):
        sql = "INSERT INTO " + self.__tablename
        sql += " (model_id, subject_id, score_type, label, feature) VALUES (UNHEX(%s), UNHEX(%s), %s, %s, %s)"
        sql += " ON DUPLICATE KEY UPDATE score = score + %s"
        g.cursor.execute(sql, (self.model_id, subject_id, ModelClassifier.FEATURE_TYPE, ModelClassifier.NULL_MAGIC_VALUE, feature, incr))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def increment_label_feature(self, subject_id, label, feature, incr):
        sql = "INSERT INTO " + self.__tablename
        sql += " (model_id, subject_id, score_type, label, feature) VALUES (UNHEX(%s), UNHEX(%s), %s, %s, %s)"
        sql += " ON DUPLICATE KEY UPDATE score = score + %s"
        g.cursor.execute(sql, (self.model_id, subject_id, ModelClassifier.LABEL_FEATURE_TYPE, label, feature, incr))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def clear(self):
        sql = "DELETE FROM " + self.__tablename +" where model_id = UNHEX(%s)"
        g.cursor.execute(sql, (self.model_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def get_labels(self, subject_id):
        sql = "SELECT label, score FROM "
        sql += self.__tablename + " WHERE model_id = UNHEX(%s) and subject_id = UNHEX(%s) and score_type = 0"
        g.cursor.execute(sql, (self.model_id, subject_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        response = {}
        if data:
            for i in data:
                response[i[0]] = i[1]
        return response

    def get_document_features(self, subject_id, features):
        # todo : get top N features
        sql = "SELECT feature, score FROM "
        sql += self.__tablename + " WHERE model_id = UNHEX(%s) and subject_id = UNHEX(%s) and score_type = 1 and feature in %s"
        g.cursor.execute(sql, (self.model_id, subject_id, features))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        response = {}
        if data:
            for i in data:
                response[i[0]] = i[1]
        return response

    def sum_all_features(self, subject_id):
        sql = "SELECT sum(score) FROM "
        sql += self.__tablename + " WHERE model_id = UNHEX(%s) and subject_id = UNHEX(%s) and score_type = 1"
        g.cursor.execute(sql, (self.model_id, subject_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchone()
        return data[0] or 0

    def get_label_features(self, subject_id, label, features):
        sql = "SELECT feature, score FROM "
        sql += self.__tablename + " WHERE model_id = UNHEX(%s) and subject_id = UNHEX(%s) and score_type = 2 and feature in %s "
        sql += " and label = %s "
        g.cursor.execute(sql, (self.model_id, subject_id, features, label))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        response = {}
        if data:
            for i in data:
                response[i[0]] = i[1]
        return response

    def sum_feature_values(self, subject_id, label):
        sql = "SELECT sum(score) FROM "
        sql += self.__tablename + " WHERE model_id = UNHEX(%s) and subject_id = UNHEX(%s) and score_type = 2 and label = %s"
        g.cursor.execute(sql, (self.model_id, subject_id, label,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchone()
        return data[0] or 0

    @staticmethod
    def reset():
        sql = "TRUNCATE " + ModelClassifier.__tablename
        g.cursor.execute(sql)
