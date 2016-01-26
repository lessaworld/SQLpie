# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie
import math, json

class Matcher(object):

    def __init__(self):
        pass

    @staticmethod
    def match_single(source_bucket, document_id, search_bucket, max_matches=1, filter_query=""):
        # Read Doc, Get top N top idf terms, and use those in the query.
        engine = sqlpie.Searcher(filter_query)
        results = engine.run_docmatching(source_bucket, document_id, search_bucket, max_matches)
        return results

    @staticmethod
    def match_all(source_bucket, search_bucket, max_matches, filter_query, output_predicate=None):
        engine = sqlpie.Searcher(filter_query)

        num_observations = 0
        if output_predicate is None:
            output_predicate = "match_" + source_bucket.lower().strip() + "_" + search_bucket.lower().strip()

        #   Delete observations from specific predicate (match_<bucket>_<search_bucket>)
        sqlpie.Observation.remove({"predicate":output_predicate})

        sb = sqlpie.Bucket(source_bucket)
        sql = ["bucket_id = UNHEX(%s)", sb.bucket_id]
        docs = sqlpie.Document.select(sql)
        is_encoded_document_id = True
        #     Loop each document from bucket
        for d in docs:
            document_id = d[1]
            #     Get scored best matches for each document
            results = engine.run_docmatching(source_bucket, document_id, search_bucket, max_matches, is_encoded_document_id)
            observations = []
            for r in results:
                #   Store scored matches/results as observations
                num_observations = num_observations + 1
                observation = {"subject_bucket":source_bucket, "object_bucket":search_bucket, "subject_id":document_id, \
                                "predicate":output_predicate, "object_id":r[sqlpie.Document.ID_FIELD], \
                                "value":r[sqlpie.Document.SCORE_FIELD]}
                observations.append(sqlpie.Observation(observation))
            if len(observations) > 0:
                sqlpie.Observation.add_multiple(observations)
        return (num_observations, output_predicate)

    @staticmethod
    def match_document(document, search_bucket, max_matches, filter_query):
        term_ids = sqlpie.Indexer.parse_features(document, False, True)
        engine = sqlpie.Searcher(filter_query)
        results = engine.run_docmatching(None, None, search_bucket, max_matches, False, term_ids)
        return results
