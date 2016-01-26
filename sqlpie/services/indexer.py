# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import sqlpie
import re, string
from stemming.porter2 import stem
import unicodedata

class Indexer(object):
    REBUILD_PARAM = "rebuild"

    def __init__(self):
        pass

    @staticmethod
    def index_documents():
        has_documents_to_index=False
        for bucket_id, doc_id in sqlpie.Document.select(["state = %s", sqlpie.Document.IS_NOT_INDEXED]):
            has_documents_to_index=True
            d = sqlpie.Document.get(bucket_id, doc_id)
            i = sqlpie.Indexer()
            i.index(d)
        if has_documents_to_index:
            sqlpie.Indexer.update_scores()

    def index(self, document):
        latitude, longitude = None, None
        self.document = document
        if self.document.state == sqlpie.Document.IS_INDEXED:
            return
        doc_json = self.document.document
        contents = sqlpie.util.walk(doc_json)
        terms_dict = {}
        for c in contents:
            content_type_from_walk, content_key_from_walk, content_value_from_walk = c
            if not content_key_from_walk.startswith("_"):
                content_key = sqlpie.ContentKey(content_key_from_walk)
                content_key.increment()
                new_content = sqlpie.Content(self.document.bucket_id, self.document.document_id, \
                                content_key.key_id, content_type_from_walk, content_value_from_walk)
                new_content.add()

                if content_key_from_walk == "latitude.":
                    latitude = content_value_from_walk

                if content_key_from_walk == "longitude.":
                    longitude = content_value_from_walk

                tokens = self.tokenizer(unicode(content_value_from_walk))
                for idx in xrange(0, len(tokens)):
                    original = tokens[idx][0]
                    t = tokens[idx][1]
                    term = sqlpie.Term(self.document.bucket_id, t)
                    term.increment()

                    content_term = sqlpie.ContentTerm(self.document.bucket_id, self.document.document_id, \
                                                        content_key.key_id, term.term_id, idx, original)
                    content_term.add()

                    if term.term_id in terms_dict:
                        terms_dict[term.term_id] += 1
                    else:
                        terms_dict[term.term_id] = 1

        terms_dict_size = len(terms_dict.keys())
        for term_id in terms_dict.keys():
            normalized_frequency = terms_dict[term_id] / float(terms_dict_size)        # Or try 1 + log(terms_dict[term_id])
            ranking_tf = sqlpie.RankingTF(self.document.bucket_id, self.document.document_id, term_id, normalized_frequency)
            ranking_tf.add()

            ranking_idf = sqlpie.RankingIDF(self.document.bucket_id, term_id)
            ranking_idf.increment()

        sqlpie.RankingIDF.update_idf(self.document.bucket_id)

        self.document.update(sqlpie.Document.STATE, sqlpie.Document.IS_INDEXED)

        # Populate GeoDocument (if applicable)
        if latitude and longitude:
            sqlpie.GeoDocument.add(self.document.bucket_id, self.document.document_id, latitude, longitude)

    @staticmethod
    def rebuild():
        sqlpie.Content.reset()
        sqlpie.Term.reset()
        sqlpie.ContentKey.reset()
        sqlpie.ContentTerm.reset()
        sqlpie.RankingIDF.reset()
        sqlpie.RankingTF.reset()

    @staticmethod
    def update_scores():
        # create tdidf_score on ranking tfidf (bucket_id, document_id)
        sqlpie.Document.update_scores()

    def tokenizer(self, content):
        """
        todo: improve this tokenizer
        """
        content = Indexer.normalize_term_without_stemming(content)
        tokens = [t for t in self._tokenize(content) if not sqlpie.global_cache[sqlpie.Config.STOPWORDS].get(t[0])]
        return tokens

    @staticmethod
    def normalize_term(s, is_query_term=False):
        s = Indexer.normalize_term_without_stemming(s, is_query_term)
        term = stem(s)
        return term

    @staticmethod
    def normalize_term_without_stemming(s, is_query_term=False, is_wildcard=False):
        # Replace special chars: e.g. Antonia's, Misérables
        s1 = unicodedata.normalize('NFD', unicode(s)).encode('ascii', 'ignore')
        term = Indexer.remove_punctuation(s1.lower(), is_query_term, is_wildcard).strip()
        return term

    @staticmethod
    def remove_punctuation(s, is_query_term, is_wildcard):
        """
        """
        exclude = set(string.punctuation)
        if is_wildcard:
            include = set(["*"])
            resp = ''.join(ch for ch in s if ch not in exclude or ch in include)
        elif is_query_term:
            exclude = set(list(exclude) + ["\""])
            resp = ''.join(ch for ch in s if ch not in exclude)
        else:
            include = set(["\"",":","-","_","*","(",")","=","<",">","&",".","/"])
            resp = ''.join(ch for ch in s if ch not in exclude or ch in include)
        return resp

    # private

    def _tokenize(self, text):
        ts = []
        for t in re.split("\W+", text):
            normalized = Indexer.normalize_term(t)
            if len(normalized) > 0:
                ts.append([t, normalized])
        return ts

    @staticmethod
    def parse_features(doc, relevant_features=False, return_ids=False):
        indexer = sqlpie.Indexer()
        features = []
        contents = sqlpie.util.walk(doc)
        if relevant_features:
            for f in relevant_features:
                for content_type_from_walk, content_key_from_walk, content_value_from_walk in contents:
                    if f + "." == content_key_from_walk:
                        if sqlpie.Predicate.convert_type(content_type_from_walk, True) in [sqlpie.Predicate.IS_FLOAT, \
                            sqlpie.Predicate.IS_BOOLEAN, sqlpie.Predicate.IS_UNICODE, sqlpie.Predicate.IS_INT]:
                            text = content_value_from_walk
                        else:
                            text = json.dumps(content_value_from_walk)
                        if return_ids:
                            features += [sqlpie.Util.to_sha1(t[1]) for t in indexer.tokenizer(text.strip())]
                        else:
                            features.append(text.lower().strip())
                            features += [t[1] for t in indexer.tokenizer(text.strip())]
        else:
            for content_type_from_walk, content_key_from_walk, content_value_from_walk in contents:
                if sqlpie.Predicate.convert_type(content_type_from_walk, True) in [sqlpie.Predicate.IS_FLOAT, \
                    sqlpie.Predicate.IS_BOOLEAN, sqlpie.Predicate.IS_UNICODE, sqlpie.Predicate.IS_INT]:
                    text = content_value_from_walk
                else:
                    text = json.dumps(content_value_from_walk)
                if return_ids:
                    features += [sqlpie.Util.to_sha1(t[1]) for t in indexer.tokenizer(text.strip())]
                else:
                    features.append(text.lower().strip())
                    features += [t[1] for t in indexer.tokenizer(text.strip())]
        return features
