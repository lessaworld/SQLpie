# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie

class Model(object):
    __tablename = "models"

    class record(object):
        def __init__(self, p):
            self.id, self.model, self.subject_bucket, self.predicate, self.model_id = p[0], p[1], p[2], p[3], p[4]
            self.bucket_id, self.predicate_id, self.last_observation = p[5], p[6], p[7]

    def create(self, model, subject_bucket, predicate, model_id, subject_bucket_id, predicate_id, last_observation=971920500):
        sql = "INSERT INTO " + self.__tablename + " (model, bucket, predicate, "
        sql += "model_id, bucket_id, predicate_id, last_observation) "
        sql += "VALUES (%s, %s, %s, UNHEX(%s), UNHEX(%s), UNHEX(%s), FROM_UNIXTIME(%s)) "
        sql += " ON DUPLICATE KEY UPDATE last_observation=FROM_UNIXTIME(%s)"
        g.cursor.execute(sql, (model, subject_bucket, predicate, model_id, subject_bucket_id, predicate_id, last_observation, last_observation))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def set_last_observation(self, model_id, last_observation):
        sql = "UPDATE " + self.__tablename + " SET last_observation = %s WHERE model_id = UNHEX(%s)"
        g.cursor.execute(sql, (last_observation, model_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def get(self, model_id):
        sql = "SELECT id, model, bucket, predicate, HEX(model_id), HEX(bucket_id), HEX(predicate_id), last_observation FROM "
        sql += self.__tablename + " WHERE model_id = UNHEX(%s)"
        g.cursor.execute(sql, (model_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        db_record = g.cursor.fetchone()
        response = None
        if db_record:
            response = Model.record(db_record)
        return response

    @staticmethod
    def reset():
        sql = "TRUNCATE " + Model.__tablename
        g.cursor.execute(sql)

