# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

#
# Similarity/Personalization/Recommendation
# What document is person P likely to love? What other people are similar to person P?
#

from flask import g
import sqlpie
import json

class Recommender(object):

    def __init__(self, subject_bucket, object_bucket, subject_id, object_id, predicate):
        self.subject_bucket_id =  sqlpie.Bucket(subject_bucket).bucket_id
        self.object_bucket_id = sqlpie.Bucket(object_bucket).bucket_id
        self.predicate_id = sqlpie.Predicate(predicate).predicate_id
        if object_id is None:
            self.subject_id = sqlpie.Util.to_sha1(unicode(subject_id))
            self.target = "subject"
            self.target_bucket_id = self.subject_bucket_id
            self.target_id = self.subject_id
            self.reference = "object"
            self.reference_bucket_id = self.object_bucket_id
        else:
            self.object_id = sqlpie.Util.to_sha1(unicode(object_id))
            self.target = "object"
            self.target_bucket_id = self.object_bucket_id
            self.target_id = self.object_id
            self.reference = "subject"
            self.reference_bucket_id = self.subject_bucket_id

    def similarity(self, limit=10, metric="pearson"):
        self.metric = metric
        return eval("self.similarity_"+self.metric+"("+str(limit)+")")

    def similarity_pearson(self, limit):
        sql =  "SELECT  HEX(%s_id2), " % (self.target,)
        sql += "        IF(num=1, 0, ((sum12 - (sum1 * sum2 / num)) / sqrt((sum1pow2 - pow(sum1, 2.0) / num) * "
        sql += "         (sum2pow2 - pow(sum2, 2.0) / num)))) AS r, num "
        sql += "FROM (SELECT o2.%s_id AS %s_id2, " % (self.target, self.target)
        sql += "      SUM(o1.predicate_value) AS sum1, SUM(o2.predicate_value) AS sum2, "
        sql += "      SUM(o1.predicate_value * o1.predicate_value) AS sum1pow2, "
        sql += "      SUM(o2.predicate_value * o2.predicate_value) AS sum2pow2, "
        sql += "      SUM(o1.predicate_value * o2.predicate_value) AS sum12, "
        sql += "      COUNT(*) AS num "
        sql += "FROM observations o1 , observations o2 "
        sql += "WHERE o1.%s_id = o2.%s_id "    % (self.reference, self.reference)
        sql += "AND o1.%s_bucket_id = o2.%s_bucket_id " % (self.reference, self.reference)
        sql += "AND o1.%s_bucket_id = UNHEX('%s') " % (self.reference, self.reference_bucket_id)
        sql += "AND o1.%s_bucket_id = UNHEX('%s') " % (self.target, self.target_bucket_id)
        sql += "AND o1.%s_id = UNHEX('%s') " % (self.target, self.target_id)
        sql += "AND o1.%s_id <> o2.%s_id " % (self.target, self.target)
        sql += "AND o1.predicate_id = o2.predicate_id "
        sql += "AND o1.predicate_id = UNHEX('%s') " % (self.predicate_id)
        sql += "GROUP BY o2.%s_id) AS base_calculation " % (self.target)
        sql += "HAVING r < 1 "
        sql += "ORDER BY r DESC, num DESC "
        sql += "LIMIT %s " % (limit,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        docs = []
        for row in data :
            target_id = row[0]
            observation = sqlpie.Observation.first(self.target, self.target_bucket_id, target_id)
            if observation is not None:
                score = float("{0:.6f}".format(row[1]))
                docs.append({"bucket_id":observation["bucket_id"],"document_id":observation["document_id"], \
                                 "_score":score,"num":row[2]})
        return docs

    def similarity_manhattan(self, limit):
        sql =  "SELECT  HEX(%s_id2), " % (self.target,)
        sql += "        (distance / n) as distance, n "
        sql += "FROM    (SELECT o2.%s_id AS %s_id2, " % (self.target, self.target)
        sql += "        SUM(ABS(o1.predicate_value - o2.predicate_value)) AS distance, "
        sql += "        COUNT(*) AS n "
        sql += "FROM observations o1 , observations o2 "
        sql += "WHERE o1.%s_id = o2.%s_id "    % (self.reference, self.reference)
        sql += "AND o1.%s_bucket_id = o2.%s_bucket_id " % (self.reference, self.reference)
        sql += "AND o1.%s_bucket_id = UNHEX('%s') " % (self.reference, self.reference_bucket_id)
        sql += "AND o1.%s_bucket_id = UNHEX('%s') " % (self.target, self.target_bucket_id)
        sql += "AND o1.%s_id = UNHEX('%s') " % (self.target, self.target_id)
        sql += "AND o1.%s_id <> o2.%s_id " % (self.target, self.target)
        sql += "AND o1.predicate_id = o2.predicate_id "
        sql += "AND o1.predicate_id = UNHEX('%s') " % (self.predicate_id)
        sql += "GROUP BY o2.%s_id) AS base_calculation " % (self.target)
        sql += "ORDER BY distance DESC, n DESC "
        sql += "LIMIT %s " % (limit,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        docs = []
        for row in data :
            target_id = row[0]
            observation = sqlpie.Observation.first(self.target, self.target_bucket_id, target_id)
            if observation is not None:
                score = float("{0:.6f}".format(row[1]))
                docs.append({"bucket_id":observation["bucket_id"],"document_id":observation["document_id"], \
                                "_score":score,"num":row[2]})
        return docs

    def recommendation(self, limit=10, metric="pearson", num=10):
        self.limit = limit           # number of similar entities to use (i.e. the k nearest neighbor)
        self.num = num               # maximum number of recommendations to make
        self.metric = metric         # distance metric
        docs = eval("self.similarity_"+self.metric+"("+str(self.limit)+")")
        total_score = 0.0
        for doc in docs:
            total_score += doc["_score"]
        results = []
        for doc in docs:
            # compute weight of similar item
            weight = doc["_score"] / total_score
            candidates = self.recommendation_candidates(doc["bucket_id"], doc["document_id"], weight)
            for row in candidates :
                reference_id = row[0]
                observation = sqlpie.Observation.first(self.reference, self.reference_bucket_id, reference_id)
                if observation is not None:
                    score = float("{0:.6f}".format(row[1]))
                    results.append({"bucket_id":observation["bucket_id"], \
                                    "document_id":observation["document_id"], "_score":score})
        results.sort(key=lambda doc: doc["_score"], reverse = True)
        results = results[:self.num]
        return results

    def recommendation_candidates(self, bucket_id, document_id, weight):
        bucket_id = sqlpie.Bucket(bucket_id).bucket_id
        document_id = sqlpie.Util.to_sha1(unicode(document_id))

        sql =  "SELECT HEX(o2.%s_id) AS %s_id2, " % (self.reference, self.reference)
        sql += "       SUM(o2.predicate_value * %s) AS score " % (weight)
        sql += "FROM observations o2 WHERE "
        sql += "o2.%s_bucket_id = UNHEX('%s') " % (self.target, bucket_id)
        sql += "AND o2.%s_id = UNHEX('%s') " % (self.target, document_id)
        sql += "AND o2.predicate_id = UNHEX('%s') " % (self.predicate_id)
        sql += "AND NOT EXISTS (SELECT 1 FROM observations o1 "
        sql += "    WHERE o1.%s_id = UNHEX('%s') " % (self.target, self.target_id)
        sql += "    AND o1.%s_bucket_id = UNHEX('%s') " % (self.target, self.target_bucket_id)
        sql += "    AND o1.predicate_id = UNHEX('%s') " % (self.predicate_id)
        sql += "    AND o1.%s_id = o2.%s_id " % (self.reference, self.reference)
        sql += "    AND o1.%s_bucket_id = o2.%s_bucket_id) " % (self.reference, self.reference)
        sql += "GROUP BY o2.%s_id " % (self.reference)
        sql += "ORDER BY score DESC "
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        return data