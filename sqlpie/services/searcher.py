# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie
import json
from collections import defaultdict
import re

class Searcher(object):

    QUERY_OPERATOR = "q"
    NUM_RESULTS = "num"
    START_RESULT = "start"
    TAGCLOUD_OPERATOR = "tagcloud"
    GEO_RADIUS_OPERATOR = "georadius"
    GEO_TARGET_OPERATOR = "geotarget"
    GEO_SORT_BY = "geosortby"
    SORT_BY_RELEVANCE = "relevance"
    SORT_BY_DISTANCE = "distance"
    SORT_TAGCLOUD_BY_RELEVANCE = "relevance"
    SORT_TAGCLOUD_BY_FREQUENCY = "frequency"

    def __init__(self, query_str=""):
        self.query_original = query_str
        self.terms, self.wildcards, self.query, self.bucket = self.pre_process_query(query_str)
        if sqlpie.Util.is_debug():
            print "terms: ", self.terms
            print "wildcards: ", self.wildcards
            print "query: ", self.query
            print "bucket: ", self.bucket

        qp = sqlpie.QueryParser()
        if len(self.terms) > 0 or len(self.query) > 0:
            self.query_sql_filters = qp.parse(self.query.lower())
        else:
            self.query_sql_filters = ""

        if sqlpie.Util.is_debug():
            print "fullsql: "
            print self.query_sql_filters
        self.custom_geo_select = ""

    def __repr__(self):
        return '<Searcher %r>' % (self.query)

    def run_searcher(self, num_results, start_result):
        # Get documents IDs that match query terms
        ranked_docs = self.ranking_by_cosine_similarity(self.bucket, self.terms, \
            self.wildcards, num_results, start_result, sqlpie.Searcher.SORT_BY_RELEVANCE)

        # Get cached documents
        docs = sqlpie.Document.get_docs(ranked_docs)
        return {"query":self.query_original, "documents":docs, "num_results":len(docs)}

    def run_docmatching(self, matching_bucket, document_id, search_bucket, num_results, is_encoded_document_id=False, matching_terms_ids=[]):
        self.bucket = search_bucket
        start_result = 0
        if is_encoded_document_id:
            matching_document = document_id
        else:
            matching_document = sqlpie.Util.to_sha1(unicode(document_id))

        ranked_docs = self.ranking_by_cosine_similarity(self.bucket, self.terms, self.wildcards, num_results, \
            start_result, sqlpie.Searcher.SORT_BY_RELEVANCE, matching_bucket, matching_document, matching_terms_ids)

        # Get cached documents
        docs = sqlpie.Document.get_docs(ranked_docs)
        return docs

    def run_tagcloud(self, tagcloud_type, num_results):
        tags = self.tagcloud_terms(self.bucket, self.terms, self.wildcards, tagcloud_type, num_results)
        return {"query":self.query_original, "tags":tags}

    def run_geosearch(self, geo_radius_search, geo_target_search, num_results, start_result, geo_sort_by):
        tlat = float(geo_target_search.split(",")[0])
        tlong = float(geo_target_search.split(",")[1])
        radius = float(geo_radius_search)

        self.custom_geo_select = " (select 3959 * acos( cos( radians(%f) ) * cos( radians( gd.latitude ) ) * cos( radians( gd.longitude ) - radians(%f) ) + sin( radians(%f) ) * sin(radians(gd.latitude)) )  from geo_documents gd where gd.bucket_id = tf.bucket_id and gd.document_id = tf.document_id) as distance " % (tlat, tlong, tlat)

        if self.query_sql_filters:
            self.query_sql_filters += " AND "

        self.query_sql_filters += " EXISTS (select (3959 * acos( cos( radians(%f) ) * cos( radians( gd.latitude ) ) * cos( radians( gd.longitude ) - radians(%f) ) + sin( radians(%f) ) * sin(radians(gd.latitude)) )) as distance from geo_documents gd where tf.document_id = gd.document_id AND gd.latitude BETWEEN (%f - degrees(%f/3959)) AND (%f + degrees(%f/3959)) AND gd.longitude BETWEEN (%f - (degrees(%f/3959/cos(radians(gd.latitude))))) AND (%f + (degrees(%f/3959/cos(radians(gd.latitude ))))) having distance <= %f) " % (tlat, tlong, tlat, tlat, radius, tlat, radius, tlong, radius, tlong, radius, radius)

        ranked_docs = self.ranking_by_cosine_similarity(self.bucket, self.terms, self.wildcards, num_results, start_result, geo_sort_by)
        docs = sqlpie.Document.get_docs(ranked_docs)
        return {"query":self.query_original, "documents":docs, "num_results":len(docs)}

    def pre_process_query(self, query_str):
        terms = []
        wildcards = []
        query = []
        bucket = sqlpie.Bucket.DEFAULT
        ignore_operators = ["and","or"]
        query_str = sqlpie.Indexer.normalize_term_without_stemming(query_str)
        for quoted_part in re.findall(r':\"(.+?)\"', query_str):
            query_str = query_str.replace(quoted_part, quoted_part.replace(" ", "_"))
        tokens = [t for t in query_str.split() if (not sqlpie.global_cache[sqlpie.Config.STOPWORDS].get(t) \
                    or t in ignore_operators)]
        for t in tokens:
            if t not in ignore_operators and \
                t[0] != "-" and \
                "*" not in t and \
                not(len(t.split(":")) == 2 and t.split(":")[0] == sqlpie.Document.BUCKET_FIELD) and \
                not (len(t.split(":")) == 2 and ("=" in t or ">" in t or "<" in t or "/" in t)):
                    token_value = t.split(":")[-1]
                    for z in token_value.replace("_", " ").split():
                        term = sqlpie.Indexer.normalize_term(z, is_query_term=True)
                        terms.append(sqlpie.Term.get_key(term))
            if "*" in t:
                wildcards.append(sqlpie.Indexer.normalize_term_without_stemming(t, is_wildcard=True).replace("*","%%"))
            if len(t.split(":")) == 2 and t.split(":")[0] == sqlpie.Document.BUCKET_FIELD:
                bucket = t.split(":")[1]
            else:
                query.append(t)
        return terms, wildcards, ' '.join(query).strip(), bucket

    def ranking_by_cosine_similarity(self, bucket, terms, wildcards, num_results, start_page, sort_by, matching_bucket=None, \
            matching_document=None, matching_term_ids=[]):
        docs = []
        if (len(terms) == 0 and len(wildcards) == 0 and len(matching_term_ids) == 0) and \
        (matching_bucket is None or matching_document is None):
            sql =  "SELECT    "
            sql += "    HEX(tf.document_id)"
            if len(self.custom_geo_select) > 0:
                sql += ", " + self.custom_geo_select
            else:
                sql += ", null"
            sql += ", d.tdidf_score"
            sql += " FROM ranking_tf tf, documents d "
            sql += "WHERE tf.`bucket_id` = (SELECT buckets.bucket_id FROM buckets WHERE buckets.bucket = %s) "
            sql += "AND tf.bucket_id = d.bucket_id AND tf.document_id = d.document_id "
            if self.query_sql_filters:
                sql += "AND (" + self.query_sql_filters + ") "
            if matching_bucket is not None and matching_document is not None:
                sql += self._document_sql_filter(matching_bucket, matching_document)
            if len(matching_term_ids) > 0:
                sql += self._terms_sql_filter(matching_term_ids)
            sql += "GROUP BY tf.document_id "
            if len(self.custom_geo_select) > 0:
                sql += "ORDER BY distance asc, tdidf_score desc "
            else:
                sql += "ORDER BY tdidf_score desc "
            sql += "LIMIT %i OFFSET %i" % (num_results, start_page)

            replacements = (bucket,)
        else:
            sql =  "SELECT    "
            sql += "    HEX(tf.document_id), "
            if len(self.custom_geo_select) > 0:
                sql += self.custom_geo_select + ", "
            else:
                sql += "null, "
            sql += "    (/*dotproduct*/ SUM(tf.normalized_frequency * idf.`frequency` * "
            sql += "        IF((SELECT 1 FROM ranking_idf "
            sql += "            WHERE ranking_idf.`bucket_id` = (SELECT buckets.bucket_id FROM buckets WHERE buckets.bucket = %s) "
            if (len(terms) > 0 or len(wildcards) > 0) and matching_bucket is None and \
            matching_document is None and len(matching_term_ids) == 0:
                sql += "    AND EXISTS (SELECT 1 FROM content_terms ct  "
                sql += "         WHERE ct.bucket_id = tf.bucket_id AND ct.document_id = tf.document_id AND "
                sql += "         ct.term_id = ranking_idf.`term_id` AND ( "
                if len(terms) > 0:
                    sql += "    ct.term_id in (" +  ','.join("UNHEX('{0}')".format(t) for t in terms) +") "
                for idx, w in enumerate(wildcards):
                    if len(terms) > 0 or idx > 0:
                        sql += " OR "
                    sql += "    ct.original like \"" +  w + "\" "
                sql += "        )) "
            if matching_bucket is not None and matching_document is not None and len(matching_term_ids) == 0:
                sql += "            AND EXISTS "
                sql += "            (SELECT 1 FROM ranking_tf tf2, ranking_idf idf2 "
                sql += "            WHERE tf2.`term_id`= idf2.`term_id` AND tf2.`bucket_id` = idf2.`bucket_id` "
                sql += "            AND idf2.`term_id` = ranking_idf.`term_id` "
                sql += "            AND idf2.`bucket_id`= (SELECT b2.bucket_id FROM buckets b2 WHERE b2.bucket = '%s') " % (matching_bucket,)
                sql += "            AND tf2.document_id = UNHEX('%s')" % (matching_document,)
                sql += "            )"
            sql += "            AND ranking_idf.`id` = idf.`id` "
            sql += "            ) IS NULL, 0, idf.`frequency`) "
            sql += "    ) / "
            sql += "     ( "
            sql += "        /*query_denom*/(SELECT SQRT(SUM(POW(idf_denon.`frequency`,2))) "
            sql += "        FROM ranking_idf idf_denon  "
            sql += "        WHERE idf_denon.`bucket_id`= (SELECT buckets.bucket_id FROM buckets WHERE buckets.bucket = %s) "
            if (len(terms) > 0 or len(wildcards) > 0) and matching_bucket is None and \
            matching_document is None and len(matching_term_ids) == 0:
                sql += "    AND EXISTS (SELECT 1 FROM content_terms ct  "
                sql += "         WHERE ct.bucket_id = tf.bucket_id AND ct.document_id = tf.document_id "
                sql += "         AND ct.term_id = idf_denon.`term_id` AND ( "
                if len(terms) > 0:
                    sql += "    ct.term_id in (" +  ','.join("UNHEX('{0}')".format(t) for t in terms) +") "
                for idx, w in enumerate(wildcards):
                    if len(terms) > 0 or idx > 0:
                        sql += " OR "
                    sql += "    ct.original like \"" +  w + "\" "
                sql += "        )) "
            if matching_bucket is not None and matching_document is not None and len(matching_term_ids) == 0:
                sql += "            AND EXISTS "
                sql += "            (SELECT 1 FROM ranking_tf tf2, ranking_idf idf2 "
                sql += "            WHERE tf2.`term_id`= idf2.`term_id` AND tf2.`bucket_id` = idf2.`bucket_id` "
                sql += "            AND idf2.`term_id` = idf_denon.`term_id` "
                sql += "            AND idf2.`bucket_id`= (SELECT b2.bucket_id FROM buckets b2 WHERE b2.bucket = '%s') " % (matching_bucket,)
                sql += "            AND tf2.document_id =  UNHEX('%s')" % (matching_document,)
                sql += "            )"

            sql += "     ) "
            sql += "        * "
            sql += "        /*doc_denom*/SQRT(SUM(POW(tf.normalized_frequency * idf.`frequency`,2))) "
            sql += "     ) "
            sql += "    ) as cosine_similarity "
            sql += "FROM ranking_tf tf, ranking_idf idf "
            sql += "WHERE tf.`term_id`= idf.`term_id` AND tf.`bucket_id` = idf.`bucket_id` "
            sql += "AND idf.`bucket_id`= (SELECT buckets.bucket_id FROM buckets WHERE buckets.bucket = %s) "
            if self.query_sql_filters:
                sql += "AND (" + self.query_sql_filters + ") "
            if matching_bucket is not None and matching_document is not None:
                sql += self._document_sql_filter(matching_bucket, matching_document)
            if len(matching_term_ids) > 0:
                sql += self._terms_sql_filter(matching_term_ids)
            sql += "GROUP BY tf.document_id "
            sql += "HAVING cosine_similarity > 0 "
            if sort_by == sqlpie.Searcher.SORT_BY_DISTANCE:
                sql += "ORDER BY distance asc "
            else:
                sql += "ORDER BY cosine_similarity desc "
            sql += "LIMIT %i OFFSET %i" % (num_results, start_page)

            replacements = (bucket,bucket,bucket,)

        if sqlpie.Util.is_debug():
            print "raw sql: ", sql

        g.cursor.execute(sql, replacements)
        if sqlpie.Util.is_debug():
            print "search query: ", g.cursor._executed
        data = g.cursor.fetchall()
        for row in data :
            if row[1]:
                distance = float("{0:.6f}".format(row[1]))
            else:
                distance = row[1]
            if row[2]:
                score = float("{0:.6f}".format(row[2]))
            else:
                score = row[2]
            docs.append((row[0], distance, score))
        return (docs,sort_by)

    def tagcloud_terms(self, bucket, terms, wildcards, tagcloud_type, num_results):
        tagcloud=[]
        if len(terms) == 0 and len(wildcards) == 0:
            return tagcloud

        sql = "SELECT ct.original, n.term_id, n.num_doc, n.term_count, n.tdidf "
        sql += "FROM content_terms ct, ( "
        sql += "SELECT idf.term_id, idf.num_doc, t.term_count, sum(idf.frequency * tf.normalized_frequency) as tdidf "
        sql += "FROM ranking_tf tf, ranking_idf idf, terms t "
        sql += "WHERE tf.`term_id`= idf.`term_id` AND     tf.`bucket_id` = idf.`bucket_id` "
        sql += "AND idf.`bucket_id`= (SELECT buckets.bucket_id FROM buckets WHERE buckets.bucket = %s) "
        sql += "AND t.bucket_id = idf.bucket_id AND t.term_id = idf.term_id "
        sql += "AND EXISTS (select 1 FROM content_terms ct2    "
        sql += "WHERE  ct2.bucket_id = tf.bucket_id AND ct2.document_id = tf.document_id AND ( "
        if len(terms) > 0:
            sql += "    ct2.term_id in (" +  ','.join("UNHEX('{0}')".format(t) for t in terms) +") "
        for idx, w in enumerate(wildcards):
            if len(terms) > 0 or idx > 0:
                sql += " OR "
            sql += "    ct2.original like \"" +  w + "\" "
        sql += ")) "
        sql += " GROUP BY idf.term_id ORDER BY 3 desc LIMIT 2 "
        sql += ") n "
        sql += "WHERE "
        sql += "ct.`bucket_id`= (SELECT buckets.bucket_id FROM buckets WHERE buckets.bucket = %s) AND  "
        sql += "ct.term_id = n.term_id AND EXISTS ( "
        sql += "    SELECT 1 FROM content_terms ct2    "
        sql += "    WHERE  ct2.bucket_id = ct.bucket_id AND ct2.document_id = ct.document_id AND ( "
        if len(terms) > 0:
            sql += "    ct2.term_id in (" +  ','.join("UNHEX('{0}')".format(t) for t in terms) +") "
        for idx, w in enumerate(wildcards):
            if len(terms) > 0 or idx > 0:
                sql += " OR "
            sql += "    ct2.original like \"" +  w + "\" "
        sql += "    ) "
        sql += ") "
        sql += "GROUP BY ct.original, n.term_id "

        if tagcloud_type == sqlpie.Searcher.SORT_TAGCLOUD_BY_RELEVANCE:
            sql += "ORDER BY 4 desc "
        elif tagcloud_type == sqlpie.Searcher.SORT_TAGCLOUD_BY_FREQUENCY:
            sql += "ORDER BY 3 desc "
        sql += "LIMIT %i" % (num_results,)

        if sqlpie.Util.is_debug():
            print "raw sql: ", sql

        g.cursor.execute(sql, (bucket, bucket, ))
        if sqlpie.Util.is_debug():
            print "search query: ", g.cursor._executed
        data = g.cursor.fetchall()
        for row in data :
            tagcloud.append({"term":row[0], "num_docs":row[2], "term_count":row[3], "_score":float("{0:.6f}".format(row[4]))})
        return tagcloud

    #
    # private
    #
    def _document_sql_filter(self, bucket, document_id):
        sql = "AND EXISTS (SELECT 1 FROM ranking_tf tf2, ranking_idf idf2 "
        sql += "        WHERE tf2.`term_id`= idf2.`term_id` AND tf2.`bucket_id` = idf2.`bucket_id` "
        sql += "        AND idf2.`bucket_id`= (SELECT b2.bucket_id FROM buckets b2 WHERE b2.bucket = '%s') "
        sql += "        AND tf2.document_id =  UNHEX('%s')"
        sql += "        AND idf2.`term_id` = idf.`term_id`"
        sql += "    ) "

        sql = sql % (bucket, document_id)
        return sql

    def _terms_sql_filter(self, matching_term_ids):
        sql = "AND idf.`term_id` in (%s) " % (', '.join('UNHEX("{0}")'.format(t) for t in matching_term_ids))
        return sql
