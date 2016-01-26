# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie
import json

class Observation(object):
    __tablename = "observations"

    def __init__(self, observation={}, is_subject_id_encoded=False, is_object_id_encoded=False):
        if not all (k in observation.keys() for k in ("subject_id","predicate","object_id")):
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)

        self.subject_id = observation["subject_id"]
        self.predicate_val = observation["predicate"]
        self.object_id = observation["object_id"]

        self.predicate_value = None
        self.predicate_type = 0
        self.observation = observation
        self.is_compressed = False

        if "timestamp" in observation:
            self.created_at = sqlpie.Util.get_current_utc_from_timestamp(observation["timestamp"])
        else:
            self.created_at = sqlpie.Util.get_current_utc_timestamp()

        if "value" in observation.keys():
            self.predicate_value = json.dumps(observation["value"])
            self.predicate_type = sqlpie.Predicate.convert_type(observation["value"])

        if "subject_bucket" in observation.keys():
            self.subject_bucket = observation["subject_bucket"]
        else:
            self.subject_bucket = sqlpie.bucket.Bucket.DEFAULT

        if "object_bucket" in observation.keys():
            self.object_bucket = observation["object_bucket"]
        else:
            self.subject_bucket = sqlpie.bucket.Bucket.DEFAULT

        self.subject_bucket_id = sqlpie.Util.to_sha1(self.subject_bucket)
        self.object_bucket_id = sqlpie.Util.to_sha1(self.object_bucket)

        if not is_subject_id_encoded:
            self.subject_id = sqlpie.Util.to_sha1(self.subject_id)
        if not is_object_id_encoded:
            self.object_id = sqlpie.Util.to_sha1(self.object_id)

    def __repr__(self):
        return '<Observation %r>' % (self.observation)

    def add(self):
        self._prepare_observation_for_put_action()
        sql = "INSERT INTO " + Observation.__tablename
        sql += " (subject_bucket_id, subject_id, object_bucket_id, object_id, "
        sql += " predicate_id, predicate_type, predicate_value, created_at, observation, is_compressed) "
        sql += " VALUES (UNHEX(%s), UNHEX(%s), UNHEX(%s), UNHEX(%s), UNHEX(%s), %s, %s, %s, %s, %s)"
        g.cursor.execute(sql, (self.subject_bucket_id, self.subject_id, self.object_bucket_id, \
            self.object_id, self.predicate_id, self.predicate_type, self.predicate_value, self.created_at, \
            self.observation, self.is_compressed))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def add_multiple(observations):
        sql_statements = []
        sql_replacement = []
        for e in observations:
            e._prepare_observation_for_put_action()
            sql_statements.append("(UNHEX(%s), UNHEX(%s), UNHEX(%s), UNHEX(%s), UNHEX(%s), %s, %s, %s, %s, %s)")
            sql_replacement.append(e.subject_bucket_id)
            sql_replacement.append(e.subject_id)
            sql_replacement.append(e.object_bucket_id)
            sql_replacement.append(e.object_id)
            sql_replacement.append(e.predicate_id)
            sql_replacement.append(e.predicate_type)
            sql_replacement.append(e.predicate_value)
            sql_replacement.append(e.created_at)
            sql_replacement.append(e.observation)
            sql_replacement.append(e.is_compressed)

        sql = "INSERT INTO " + Observation.__tablename + " (subject_bucket_id, subject_id, object_bucket_id, object_id, "
        sql += "predicate_id, predicate_type, predicate_value, created_at, observation, is_compressed) VALUES "
        sql += ",".join(sql_statements)
        g.cursor.execute(sql, tuple(sql_replacement))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def remove(conditions):
        sql_statements, sql_replacement, options = Observation._conditions_to_sql(conditions)

        sql = "DELETE FROM %s WHERE " % (Observation.__tablename,)
        sql += " AND ".join(sql_statements)

        g.cursor.execute(sql, tuple(sql_replacement))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

        sql = "SELECT ROW_COUNT()"
        g.cursor.execute(sql,)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        response = g.cursor.fetchone()
        record_count = response[0]
        return record_count

    @staticmethod
    def get(conditions):
        sql_statements, sql_replacement, options = Observation._conditions_to_sql(conditions)

        sql = "SELECT SQL_CALC_FOUND_ROWS NULL, observation, is_compressed FROM %s WHERE " % (Observation.__tablename,)
        sql += " AND ".join(sql_statements)
        sql += " LIMIT %s, %s" % (options["offset"], options["limit"])
        sql += " UNION SELECT FOUND_ROWS(), NULL, NULL "

        g.cursor.execute(sql, tuple(sql_replacement))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()

        total = 0
        d = []
        if data:
            for i in data:
                if i[0]:
                    total = i[0]
                elif i[1] and i[2]:
                    r_observation = i[1]
                    r_is_compressed = i[2]
                    if r_is_compressed == True:
                        r_observation = sqlpie.Util.uncompress(r_observation)
                    d.append(json.loads(r_observation))
        return (d, total)

    @staticmethod
    def first(reference, reference_bucket_id, reference_id):
        if reference == "object":
            sql_statements = "object_bucket_id = UNHEX(%s) and object_id = UNHEX(%s) "
        else:
            sql_statements = "subject_bucket_id = UNHEX(%s) and subject_id = UNHEX(%s) "
        sql = "SELECT observation, is_compressed FROM " + Observation.__tablename + " WHERE "
        sql += sql_statements
        sql += "LIMIT 1"
        g.cursor.execute(sql, (reference_bucket_id, reference_id, ))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchone()
        resp = None
        if data:
            r_observation = data[0]
            r_is_compressed = data[1]
            if r_is_compressed == True:
                r_observation = sqlpie.Util.uncompress(r_observation)
            observation = json.loads(r_observation)
            if reference == "object":
                resp = {"bucket_id":observation["object_bucket"], "document_id":observation["object_id"]}
            else:
                resp = {"bucket_id":observation["subject_bucket"], "document_id":observation["subject_id"]}
        return resp

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Observation.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def stats():
        sql = "SELECT COUNT(1) FROM %s" % (Observation.__tablename,)
        g.cursor.execute(sql)
        data = g.cursor.fetchone()
        if data is None:
            ret = 0
        else:
            ret = data[0]
        return ret

    #
    # private
    #

    def _prepare_observation_for_put_action(self):
        p = sqlpie.Predicate(self.predicate_val)
        p.increment()
        self.predicate_id = p.predicate_id
        raw_data = json.dumps(self.observation)
        self.compressed_data = sqlpie.Util.compress(raw_data)
        if len(self.compressed_data) < len(raw_data) + (len(raw_data) * .1):
            self.observation = self.compressed_data
            self.is_compressed = True
        else:
            self.observation = raw_data
            self.is_compressed = False


    @staticmethod
    def _conditions_to_sql(conditions):
        sql_statements = []
        sql_replacement = []
        tokens_requiring_encoding = ["subject_bucket","subject_id","object_bucket","object_id","predicate"]
        bucket_tokens = ["subject_bucket", "object_bucket"]
        predicate_token = ["predicate"]
        timestamp_token = ["created_at"]
        field_replacements = {"subject_bucket":"subject_bucket_id", "object_bucket":"object_bucket_id",
            "subject_id":"subject_id", "object_id":"object_id", "predicate":"predicate_id", "value":"predicate_value",
            "timestamp":"created_at","options":"options"}
        valid_tokens = field_replacements.keys()

        options = {"limit":10, "offset":0}
        if "options" in conditions.keys():
            if "limit" in conditions["options"]:
                options["limit"] = conditions["options"]["limit"]
            if "offset" in conditions["options"]:
                options["offset"] = conditions["options"]["offset"]

        for k in conditions.keys():
            k = k.lower()
            if k in valid_tokens:
                v = conditions[k]
                v_type = type(v).__name__
                if v_type == "list":
                     if len(v) > 0:
                        if k in tokens_requiring_encoding:
                            sql_string_list = []
                            for item in v:
                                if k in bucket_tokens:
                                    b = sqlpie.Bucket(item)
                                    lv = b.bucket_id
                                elif k in predicate_token:
                                    p = sqlpie.Predicate(item)
                                    lv = p.predicate_id
                                else:
                                    lv = sqlpie.Term.get_key(item)
                                sql_string_list.append("UNHEX(%s)")
                                sql_replacement.append(lv)
                        else:
                            sql_string_list = []
                            for item in v:
                                sql_string_list.append("%s")
                                sql_replacement.append(item)
                        k = field_replacements[k]
                        sql_statements.append(k + " in (" + ",".join(sql_string_list) + ")")
                else:
                    if k in tokens_requiring_encoding:
                        if k in bucket_tokens:
                            b = sqlpie.Bucket(v)
                            v = b.bucket_id
                        elif k in predicate_token:
                            p = sqlpie.Predicate(v)
                            v = p.predicate_id
                        else:
                            v = sqlpie.Term.get_key(v)
                        k = field_replacements[k]
                        sql_statements.append(k + " = UNHEX(%s)")
                        sql_replacement.append(v)
                    else:
                        k = field_replacements[k]
                        if type(v).__name__ == "dict":
                            if v.has_key("start") or v.has_key("end"):
                                if v.has_key("start"):
                                    if k in timestamp_token:
                                        condition = k + " >= FROM_UNIXTIME(%s)"
                                    else:
                                        condition = k + " >= %s"
                                    sql_statements.append(condition)
                                    sql_replacement.append(v["start"])

                                if v.has_key("end"):
                                    if k in timestamp_token:
                                        condition = k + " <= FROM_UNIXTIME(%s)"
                                    else:
                                        condition = k + " <= %s"
                                    sql_statements.append(condition)
                                    sql_replacement.append(v["end"])
                        else:
                            sql_statements.append(k + " = %s")
                            sql_replacement.append(v)
            else:
                raise sqlpie.CustomException(sqlpie.CustomException.INVALID_ARGUMENTS)
        return (sql_statements, sql_replacement, options)
