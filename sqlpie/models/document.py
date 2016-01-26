# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import json
import sqlpie
import os

class Document(object):
    __tablename = "documents"
    STATE = "state"
    IS_NOT_INDEXED = 0
    IS_INDEXED = 1
    PARSERS_PARAM = "parsers"
    BUCKET_FIELD = "_bucket"
    ID_FIELD = "_id"
    SCORE_FIELD = "_score"
    DISTANCE_FIELD = "_distance"

    def __init__(self, document={}, parsers=[]):
        """
        Args:
            document (object)    :
            bucket (str)        : Name of the bucket
        """
        if sqlpie.Document.ID_FIELD in document.keys():
            self.document_id = sqlpie.Util.to_sha1(unicode(document[sqlpie.Document.ID_FIELD]))
        else:
            unique_identifier = sqlpie.Util.get_unique_identifier()
            self.document_id = sqlpie.Util.to_sha1(unique_identifier)
            document[sqlpie.Document.ID_FIELD] = unique_identifier

        if sqlpie.Document.BUCKET_FIELD in document.keys():
            self.bucket = document[sqlpie.Document.BUCKET_FIELD]
        else:
            self.bucket = sqlpie.Bucket.DEFAULT

        self.document = document
        self.id = None
        self.bucket_id = None
        self.is_compressed = None
        self.state = Document.IS_NOT_INDEXED
        self.created_at = None
        self.data = None

        self.parsers = {}
        for p in parsers:
            filename = os.path.dirname(os.path.realpath(__file__)) + "/../parsers/"+p+".py"
            if os.path.isfile(filename):
                try:
                    source = open(filename,"r").read()
                    code = compile(source, '<string>', 'exec')
                    self.parsers[p] = code
                except:
                    raise sqlpie.CustomException(sqlpie.CustomException.INVALID_PARSER)

    def __repr__(self):
        return '<Document %r>' % (self.document)

    def update(self, param, value):
        sql = "UPDATE " + self.__tablename + " SET " + param + " = %s WHERE document_id = UNHEX(%s)"
        g.cursor.execute(sql, (value, self.document_id))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    def add(self):
        self._prepare_doc_for_put_action()
        sql = "INSERT INTO " + self.__tablename
        sql += " (bucket_id, document_id, document, is_compressed, created_at) VALUES (UNHEX(%s), UNHEX(%s), %s, %s, %s)"
        sql += " ON DUPLICATE KEY UPDATE state=%s"
        g.cursor.execute(sql, (self.bucket_id, self.document_id, self.data, self.is_compressed, self.created_at, Document.IS_NOT_INDEXED))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def get_docs(search_response):
        ranked_docs, sort_by = search_response[0], search_response[1]
        if len(ranked_docs) == 0:
            return []
        list_of_doc_ids = []
        doc_scores, doc_distances = {}, {}
        for d, distance, score in ranked_docs:
            if distance is not None:
                doc_distances[d] = distance
            if score is not None:
                doc_scores[d] = score
            list_of_doc_ids.append("UNHEX('%s')" % d)
        sql = "SELECT HEX(document_id), document, is_compressed FROM "
        sql += Document.__tablename + " WHERE document_id in (%s)" % (",".join(list_of_doc_ids))
        g.cursor.execute(sql)
        data = g.cursor.fetchall()
        docs = []
        for row in data :
            if row[2] == True:
                data = sqlpie.Util.uncompress(row[1])
            else:
                data = row[1]
            doc = json.loads(data)
            if row[0] in doc_distances:
                doc[sqlpie.Document.DISTANCE_FIELD] = float("{0:.6f}".format(doc_distances[row[0]]))
            if row[0] in doc_scores:
                doc[sqlpie.Document.SCORE_FIELD] = float("{0:.6f}".format(doc_scores[row[0]]))
            else:
                doc[sqlpie.Document.SCORE_FIELD] = 0
            docs.append(doc)
        if sort_by == sqlpie.Searcher.SORT_BY_DISTANCE:
            docs = sorted(docs, key=lambda k: k[sqlpie.Document.DISTANCE_FIELD], reverse=True)
        elif sort_by == sqlpie.Searcher.SORT_BY_RELEVANCE:
            docs = sorted(docs, key=lambda k: k[sqlpie.Document.SCORE_FIELD], reverse=True)
        return docs

    @staticmethod
    def add_multiple(documents):
        sql_statements = []
        sql_replacement = []
        for d in documents:
            d._prepare_doc_for_put_action()
            sql_statements.append("(UNHEX(%s), UNHEX(%s), %s, %s, %s)")
            sql_replacement.append(d.bucket_id)
            sql_replacement.append(d.document_id)
            sql_replacement.append(d.data)
            sql_replacement.append(d.is_compressed)
            sql_replacement.append(d.created_at)
        sql_replacement.append(Document.IS_NOT_INDEXED)
        sql = "INSERT INTO " + Document.__tablename + " (bucket_id, document_id, document, is_compressed, created_at) VALUES "
        sql += ",".join(sql_statements)
        sql += " ON DUPLICATE KEY UPDATE state=%s"

        g.cursor.execute(sql, tuple(sql_replacement))
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    @staticmethod
    def select(conditions):
        """
        Args:
            conditions (list)    :

        Returns:
            List of tuples        :

        """
        where_clause = conditions[0]
        where_variables = tuple(conditions[1:])
        sql = "SELECT HEX(bucket_id), HEX(document_id) FROM " + Document.__tablename + " WHERE " + where_clause
        g.cursor.execute(sql, where_variables)
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchall()
        return [(row[0], row[1]) for row in data]

    @staticmethod
    def get(bucket_id, doc_id):
        sql = "SELECT id, HEX(bucket_id), HEX(document_id), document, is_compressed, state, created_at FROM "
        sql += Document.__tablename + " WHERE bucket_id = UNHEX(%s) and document_id = UNHEX(%s) LIMIT 1"
        g.cursor.execute(sql, (bucket_id, doc_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        data = g.cursor.fetchone()
        d = None
        if data:
            d = Document()
            d.id, d.bucket_id, d.document_id, d.document, d.is_compressed, d.state, d.created_at = data
            if d.is_compressed == True:
                d.document = sqlpie.Util.uncompress(d.document)
            d.document = json.loads(d.document)
        return d

    @staticmethod
    def remove(bucket_id, doc_id):
        sql = "DELETE FROM "
        sql += Document.__tablename + " WHERE bucket_id = UNHEX(%s) and document_id = UNHEX(%s) LIMIT 1"
        g.cursor.execute(sql, (bucket_id, doc_id,))
        if sqlpie.Util.is_debug():
            print g.cursor._executed
        sql = "SELECT ROW_COUNT() "
        g.cursor.execute(sql)
        data = g.cursor.fetchone()
        num_docs = data[0]

        sqlpie.Bucket.decrement(bucket_id, num_docs)

        #
        sqlpie.GeoDocument.remove(bucket_id, doc_id)
        return num_docs

    @staticmethod
    def reset():
        sql = "TRUNCATE %s" % (Document.__tablename,)
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed

        sqlpie.GeoDocument.reset()

    @staticmethod
    def stats():
        sql = "SELECT COUNT(1) FROM %s" % (Document.__tablename,)
        g.cursor.execute(sql)
        data = g.cursor.fetchone()
        if data is None:
            ret = 0
        else:
            ret = data[0]
        return ret

    @staticmethod
    def update_scores():
        sql =  "UPDATE documents d "
        sql += "INNER JOIN "
        sql += "( "
        sql += "    SELECT t.bucket_id, t.document_id, "
        sql += "           1 / LOG(SUM(t.normalized_frequency * i.`frequency`)) as tdidf_score "
        sql += "    FROM ranking_tf t, ranking_idf i "
        sql += "    WHERE t.term_id = i.term_id AND t.bucket_id = i.bucket_id "
        sql += "    GROUP BY t.bucket_id, t.document_id "
        sql += ") j ON d.bucket_id = j.bucket_id AND d.document_id = j.document_id  "
        sql += "SET d.tdidf_score = j.tdidf_score "
        g.cursor.execute(sql)
        if sqlpie.Util.is_debug():
            print g.cursor._executed

    #
    # private
    #

    def _prepare_doc_for_put_action(self):
        b = sqlpie.Bucket(self.bucket)
        b.increment()
        self.bucket_id = b.bucket_id
        self.created_at = sqlpie.Util.get_current_utc_timestamp()
        self.document["_bucket"] = self.bucket

        for parser in self.parsers.keys():
            self.document = self._handle_parser(parser, self.document)

        raw_data = json.dumps(self.document)
        self.compressed_data = sqlpie.Util.compress(raw_data)
        if len(self.compressed_data) < len(raw_data) + (len(raw_data) * .1):
            self.data = self.compressed_data
            self.is_compressed = True
        else:
            self.data = raw_data
            self.is_compressed = False

    def _handle_parser(self, parser, document):
        code = self.parsers[parser]
        ns = {}
        exec code in ns
        if "parse" in ns:
            f = ns["parse"]
            if hasattr(f, '__call__'):
                document = f(document)
        return document
