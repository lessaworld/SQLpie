# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json, urllib2
import traceback

class SQLpieClient(object):
    def __init__(self, sqlpie_server, json_responses=True):
        self.sqlpie_server = sqlpie_server
        self.json_responses = json_responses

    def _handler(self, endpoint, json_request):
        try:
            if type(json_request).__name__ != "dict":
                # if the input is text, it converts into an actual object
                json_request = json.loads(json_request)
            req = urllib2.Request(self.sqlpie_server + endpoint)
            req.add_header('Content-Type', 'application/json')
            resp = urllib2.urlopen(req, json.dumps(json_request))
            r = resp.read()
            if self.json_responses:
                r = json.loads(r)
        except urllib2.HTTPError, e:
            contents = e.read()
            r = json.loads(contents)
            r["http_error_code"] = e.code
            # r = '{"HTTPError": %s, "response": "%s"}' % (str(e.code), contents)
        except urllib2.URLError, e:
            r = json.loads('{"URLError": "%s"}' % (str(e.reason),))
        except Exception:
            r = 'Error: Invalid Syntax' #+ traceback.format_exc()
        return r

    #
    # Health Checks
    #

    def ping(self, json_request={}):
        u"""/ping : Health check that sends a simple test request to the server.

        NOTES:
            - The response is a simple "pong".
            - This service accepts both GET and POST requests.

        JSON_OBJECT PARAMS:
            none

        EXAMPLE REQUEST:

            Using the SQLpie shell:

                SQLpie # /ping

            Using a command line tool:

                curl -i -X GET http://localhost:5000/ping

            Using the SQLpie client:

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.ping()

        RESPONSE:

            {
                "ping": "pong"
            }

        """
        return self._handler("/ping", json_request)

    def stats(self, json_request={}):
        u"""/stats : Shows internal state of the server installation and values of key environment variables.

        NOTES:
            - This service accepts both GET and POST requests.

        JSON_OBJECT PARAMS:
            none

        EXAMPLE REQUEST:

            Using the SQLpie shell:

                SQLpie # /stats

            Using a command line tool:

                curl -i -X GET http://localhost:5000/stats

            Using the SQLpie client:

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.stats()

        RESPONSE:

            {
                "cachebuckets": [
                    "_STOPWORDS",
                    "_OPTIONS"
                ],
                "database_name": "sqlpie_development",
                "database_schema": "1.21",
                "num_docs": 1,
                "num_observations": 0,
                "sqlpie_debug": "true",
                "sqlpie_env": "development"
            }

        """
        return self._handler("/stats", json_request)

    #
    # Documents
    #

    def document_put(self, json_request={}):
        u"""/document/put <json_object> : Adds one or more JSON documents to the SQLpie storage.

        NOTES:
            - Add one or multiple documents in a single call.
            - If an "_id" field is not provided for a document, a unique identifier is created and assigned to it.
            - If a "_bucket field is not provided for a document, the document will be assigned to the "DEFAULT" bucket.
            - If a given "_id" already exists, the new document replaces the old one.
            - An optional parser option can be provide. See section below.

        JSON_OBJECT PARAMS:
            documents        : single object or a list of objects (required)
            options->parsers : name of parsers to use (optional)


        EXAMPLE REQUEST:

            Using the SQLpie shell:

                SQLpie # /document/put {"documents":{"_id":"001", "_bucket":"employees","name":"John"}}

            Using a command line tool:

                curl -i -H "Content-Type: application/json" -X POST -d '{"documents":{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA","title":"CEO"}}' http://localhost:5000/document/put

            Using the SQLpie client:

                # Single document example:

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.document_put({"documents":{"_id":"001", "_bucket":"employees","name":"John"}})

                # Multi-document example:

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.document_put({"documents":[{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA","title":"CEO"},{"_id":"002", "_bucket":"employees","name":"Peter","location":"Cleveland, OH","title":"CFO"}]})

        RESPONSE:

            [TBD - Yet To Be Documented]

        DOCUMENT PARSERS:
        -----------------

            - Parsers are used to modify/remove/create fields in a document as they're loaded.
            - Each parser lives in its own file in the /sqlpie/parsers directory.
            - Files can be hot swapped/updated without restarting the server.
            - The file name is what is passed as a parameter in the API call.
            - Inside the file, a parser function is used to transform the document's json object.
            - After any changes are made to the document, it is expected that a new document is returned to be indexed.
            - The function name that is called by the indexing engine is "parse".
            - The available examples, show that you can test the function by directly calling this script.
                e.g. python sqlpie/parsers/location.py

            Example showing how to use parsers through the API:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.document_put({"documents":{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA"}, "options":{"parsers":["location"]}})

        """
        return self._handler("/document/put", json_request)

    def document_get(self, json_request={}):
        u"""/document/get <json_object> : Returns a single JSON document for a given identifier (ie. the value of the _id field)

        JSON_OBJECT PARAMS:
            _id     : document identifier (required)
            _bucket : document bucket (optional, defaults to the "DEFAULT" bucket)

        EXAMPLE REQUEST:

            Using a command line tool:

                curl -i -H "Content-Type: application/json" -X POST -d '{"_id":2}' http://localhost:5000/document/get

            Using the SQLpie client:

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.document_get({"_id":"006", "_bucket":"customers"})

        RESPONSE:

            [TBD - Yet To Be Documented]

            {"document":{"_id":"","_bucket":"",...}}

        """
        return self._handler("/document/get", json_request)

    def document_remove(self, json_request={}):
        u"""/document/remove <json_object> : Deletes a single JSON document for a given identifier (ie. the value of the _id field)

        JSON_OBJECT PARAMS:
            _id     : document identifier (required)
            _bucket : document bucket (optional, defaults to the "DEFAULT" bucket)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.document_remove({"_id":"006e", "_bucket":"customers"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/document/remove", json_request)

    def document_reset(self, json_request={}):
        u"""/document/reset : Deletes ALL documents in the database.

        NOTES:
            - This is a very damaging call so it requires a lot of caution (So, have CAUTION!!!)

        JSON_OBJECT PARAMS:
            none

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.document_reset({})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/document/reset", json_request)

    #
    # Observations
    #

    def observation_put(self, json_request={}):
        u"""/observation/put <json_object> : Adds one or more JSON observations to the SQLpie storage.

        NOTES:
            - Add one or multiple observations in a single call.
            - Submit either single object or a list of objects.

        JSON_OBJECT PARAMS (for each observation):
            subject_bucket  : bucket name of the observation's subject (optional, defaults to "DEFAULT")
            subject_id      : subject's document identifier (required)
            predicate       : predicate of the observation (required)
            object_bucket   : bucket name of the observation's object (optional, defaults to "DEFAULT")
            object_id       : object's document identifier (required)
            value           : value of the observation (optional)
            timestamp       : timestamp of the observation (optional, defaults to current timestamp)

            The predicate value can be one of the following types:

            Integer:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":3}
            Float:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":5.34}
            Boolean:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":True}
            List:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":["Action","Drama"]}
            None:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":None}
            String:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":"Very Good"}
            Object:
            e.g. {"subject_bucket":"people", "object_bucket":"docs", "subject_id":"001", "predicate":"likes", "object_id":"Document001", "value":{"expired":True}}


        EXAMPLE REQUEST:

            # Single Observation

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_put({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod002", "value":5, "timestamp":972654989})

            # Multiple Observations

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            observations = []
            observations.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod001", "value":3, "timestamp":972654989})
            observations.append({"subject_bucket":"customers", "object_bucket":"products", "subject_id":"001", "predicate":"likes", "object_id":"Prod002", "value":5, "timestamp":972654989})
            response = sqlrc.observation_put(observations)

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/observation/put", json_request)

    def observation_get(self, json_request={}):
        u"""/observation/get :  Returns JSON observations for a given lookup query

        NOTES:
            - All JSON_OBJECT PARAMS are optional. You can send any combination to the request.

        JSON_OBJECT PARAMS:
            subject_bucket  : bucket name of the observation's subject
            subject_id      : subject's document identifier (string or list of strings)
            predicate       : predicate of the observation
            object_bucket   : bucket name of the observation's object
            object_id       : object's document identifier (string or list of strings)
            value           : value of the observation (value or range using value->start and value->end)
            timestamp       : timestamp of the observation (value or range using timestamp->start and timestamp->end)
            options->limit  : number of results to return (defaults to 10)
            option->offset  : number of the results to skip (starts at 0)

        EXAMPLE REQUEST:

            # All observations recorded for the "customers" subject_bucket.
            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_get({"subject_bucket":"customers"})

            # All observations recorded for the "customers" subject_bucket, specifically for subject_id is 001 or 002.
            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_get({"subject_bucket":"customers", "subject_id":["001","002"]})

            # All observations recorded where the predicate is "likes
            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_get({"predicate":"likes"})

            # All observations recorded where the value is between 3 and 5.
            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_get({"subject_bucket":"customers", "subject_id":"001", "value":{"start":3, "end":5}})

            # All observations recorded where the timestamp is between 972654980 and 972655000.
            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_get({"subject_bucket":"customers", "timestamp":{"start":972654980, "end":972655000}})

            # The first 10 observations recorded for the "customers" subject_bucket.
            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_get({"subject_bucket":"customers", "options":{"limit":10, "offset":0}})

        RESPONSE:

            [TBD - Yet To Be Documented]
            TODO: Explain record_count vs total_count ... i.e. # of documents returned / # of total docs available

        """
        return self._handler("/observation/get", json_request)

    def observation_remove(self, json_request={}):
        u"""/observation/remove <json_object> : Deletes observations based on a specific selection criteria.

        NOTES:
            - Similar to observation_get, in terms of the selection criteria.

        JSON_OBJECT PARAMS:
            subject_bucket  : bucket name of the observation's subject
            subject_id      : subject's document identifier (string or list of strings)
            predicate       : predicate of the observation
            object_bucket   : bucket name of the observation's object
            object_id       : object's document identifier (string or list of strings)
            value           : value of the observation (value or range using value->start and value->end)
            timestamp       : timestamp of the observation (value or range using timestamp->start and timestamp->end)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_remove({"subject_bucket":"customers", "subject_id":"001"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/observation/remove", json_request)

    def observation_reset(self, json_request={}):
        u"""/observation/reset : Deletes ALL observations in the database.

        NOTES:
            - This is a very damaging call so it requires a lot of caution (So, have CAUTION!!!)

        JSON_OBJECT PARAMS:
            none

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.observation_reset({})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/observation/reset", json_request)

    #
    # Search
    #

    def service_index(self, json_request={}):
        u"""/service/index : Indexes all documents that haven't been indexed yet.

        NOTES:
            - The options file specifies which stopword files (if any) should be used.
            - By default, the `data/english.stop` stopworld file is loaded.
            - If a `latitude` and `longitude` attributes are provided, they're stored as coordinates.

        JSON_OBJECT PARAMS:
            option->rebuild : if used, rebuilds the entire index.

        EXAMPLE REQUEST:

            # Simple indexing call to index only new documents

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_index({})

            # With option to rebuild the entire index.

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_index({"options":{"rebuild":True}})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/index", json_request)

    def service_search(self, json_request={}):
        u"""/service/search : Searches for indexed documents using Boolean/Vector search. GeoSearch and TagCloud also available.

        NOTES:
            - The search grammar should be similar to most full text search engines (Google, Lucene, etc..).
            - The search query parser supports: 'and', 'or', implicit 'and', and not-word operators, parenthesis, quoted strings, field searches, and wildcards.
            - There are essentially 3 types of search: standard search, geosearch, and tagcloud search

        JSON_OBJECT PARAMS:
            q           : search query expression (required)
            num         : number of results to return (optional, defaults to 10)
            start       : offset of where to start in the result set (optional)
            georadius   : radius for the geosearch (only applicable if geotarget is also provided)
            geotarget   : target lat/long for the geosearch (only applicable if georadius is also provided)
            geosortby   : sort geosearch results by "relevance" or by "distance" (default is "distance")
            tagcloud    : return tagcloud results either by "relevance" or by "frequency" (optional)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_search({"q":"apple"})

            Other search query expression examples:

            {"q":'"Iron Eagle"'}
            {"q":'"Iron Eagle" _bucket:movies'}
            {"q":"Iron _bucket:movies"}
            {"q":"Iron -man _bucket:movies"}
            {"q":"(eagle OR man) _bucket:movies"}
            {"q":"Iron AND man _bucket:movies"}
            {"q":"(man) _bucket:movies"}
            {"q":"(iron) _bucket:movies"}
            {"q":"(iron OR eagle) -man _bucket:movies"}
            {"q":"name:terminator _bucket:movies"}
            {"q":'(name:terminator) OR "star wars" _bucket:movies'}
            {"q":"termin* or goon* _bucket:movies"}
            {"q":'ter* or "goonies" _bucket:movies'}
            {"q":"name:Harry or name:terminator _bucket:movies"}
            {"q":"the _bucket:movies"}
            {"q":"the matrix _bucket:movies"}
            {"q":"harry _bucket:movies","num":1,"start":1}
            {"q":"harry _bucket:movies","num":2,"start":2}
            {"q":"harry _bucket:movies","num":2,"start":1}
            # unicode case
            {"q":"Antonia's or Misérables or naïve or café _bucket:tests"}
            # stem case
            {"q":"Antonia _bucket:tests"}
            {"q":'"Eagle of Iron" _bucket:movies'}
            {"q":"_bucket:orders"}
            {"q":'total:=250 _bucket:orders'}
            {"q":"total:>250 _bucket:orders"}
            {"q":"total:>=300 _bucket:orders"}
            {"q":"total:<250 _bucket:orders"}
            {"q":"total:<=250 _bucket:orders"}
            {"q":"total:>=250&<=300 _bucket:orders"}
            {"q":"total:>200&<300 _bucket:orders"}
            {"q":"shipping.state:pa _bucket:orders"}
            {"q":"shipping.state:ca _bucket:orders"}
            {"q":"shipping.state:ca billing.city:florida _bucket:orders"}
            {"q":".city:pittsburgh _bucket:orders"}
            {"q":".cost:>50 _bucket:orders"}
            {"q":".cost:>84.1&<84.9 _bucket:orders"}
            {"q":'.city:"los angeles" _bucket:orders'}
            {"q":"order_date:>07/01/2015 _bucket:orders"}
            {"q":"order_date:>07/01/2015&<11/01/2015 _bucket:orders"}
            {"q":"order_date:<11/01/2015 _bucket:orders"}
            {"q":"shipping.shipping_date:Oct/02/2015 _bucket:orders"}
            {"q":"shipping.shipping_date:=Oct/02/2015 _bucket:orders"}
            {"q":".shipping_date:=Oct/02/2015 _bucket:orders"}
            {"q":".shipping_date:>=Oct/02/2015&<=Oct/02/2015 _bucket:orders"}
            {"q":"shipping_date:=Oct/02/2015 _bucket:orders"}
            {"q":"total:>-250 _bucket:orders"}
            {"q":"total:>-250&<=50 _bucket:orders"}
            {"q":".shipped:=true _bucket:orders"}
            {"q":".shipped:=false _bucket:orders"}

            Geo Search:
            -----------

            GeoSearch uses 2 search params:
                - `georadius` (numeric) and `geotarget` in either a specific lat,long or field:value, which is parsed to lat/long.
                - `geosortby` is an optional field, which can be either relevance or distance (the default).
                -  GeoSearch works by looking for 2 specific fields in the documents: `latitude` and `longitude`.

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.service_search({"q":"_bucket:employees","georadius":20,"geotarget":"40.4405556,-79.9961111"})

                # when sorted by relevance...

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.service_search({"q":"john _bucket:employees", "georadius":20, "geotarget":"40.4405556,-79.9961111", "geosortby":"relevance"})

            Tagcloud Search:
            -----------------

            Returns a list of common terms and phrases.
            Instead of documents, it returns: the terms, num_docs, term_count, relevance
            Results are sorted in 2 ways: by term relevance, by term frequency

                # Tagcloud by term relevance

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.service_search({"q":"john _bucket:employees", "tagcloud":"relevance"})

                # Tagcloud by term frequency

                import sqlpie_client
                sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
                response = sqlrc.service_search({"q":"john _bucket:employees", "tagcloud":"frequency"})

            The Tagcloud results is a list of terms.
            For each term, its term_count, _score, and num_docs are provided.

        RESPONSE:

            [TBD - Yet To Be Documented]
            TODO: Explain _score field that is returned for each document in the standard search results.
            TODO: Explain _distance and _score fields that are returned for each document in the geosearch results.
            TODO: Explain _ratio and _score fields that are returned for each document in the tagcloud search results.

        """
        return self._handler("/service/search", json_request)

    #
    # Matching
    #

    def service_matching(self, json_request={}):
        u"""/service/matching/ : Finds documents that match a given document.

        NOTES:
            - Document matching is essentially a search query where the search terms come from a document.
            - The document to be analyzed can come from the storage or be provided in the request itself.
            - To choose a document, either use the bucket/document_id or the document params.
            - The response that comes back contains a list of matching documents, each with a _store field.
            - If multiple results are requested, the rankings are stored as observations.

        JSON_OBJECT PARAMS:
            bucket          : bucket of the document(s) to be analyzed
            document_id     : identifier of the document to be analyzed (requires bucket)
            document        : to be used alternatively, if the bucket/document_id is not provided
            search_bucket   : bucket where the search will take place (required)
            num_results     : max number of results to return (optional, defaults to 1)
            filter_query    : query that will run on the search bucket to limit the scope of the matching (optional)


        EXAMPLE REQUEST:

            # Find documents in the `jobs` search bucket that are good matches to the bucket/document_id document

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_matching({"bucket":"candidates", "document_id":"c003", "search_bucket":"jobs"})

            # Find documents in the `jobs` search bucket, and brings back the top 5 results

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_matching({"bucket":"candidates", "document_id":"c003", "search_bucket":"jobs", "num_results":5})

            # Matches documents, but limits the scope of the search_bucket to a specific query

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_matching({"bucket":"candidates", "document_id":"c003", "search_bucket":"jobs", "filter_query":"state:PA"})

            # Loops through all documents in a bucket, and returns top 5 matches for each one.
            # In cases like this, results are stored as observations using a specific output_predicate
            # The default naming convention is "match_<bucket>_<search_bucket>". e.g. match_candidates_jobs
            # Those results need to be retrieved using `observation/get`

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_matching({"bucket":"candidates", "search_bucket":"jobs", "num_results":5})

            # To save the output with a custom predicate name.

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_matching({"bucket":"candidates", "search_bucket":"jobs", "num_results":5, "output_predicate":"monthly_report"})

            predicate = response["output_predicate"]
            results = sqlrc.observation_get({"predicate":predicate})

            # Find documents in the `jobs` search bucket that are good matches to the provided document

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_matching({"document":{"name":"John", "resume":"Software Engineer with 5 years of Python experience."}, "search_bucket":"jobs"})


        RESPONSE:

            [TBD - Yet To Be Documented]
            TODO: document total_matches, output_predicate, _score

        """
        return self._handler("/service/matching/", json_request)

    #
    # Classifier
    #

    def service_classifier(self, json_request={}):
        u"""/service/classifier/init : Initializes a new classifier model.

        NOTES:
            - This request creates the proper data structures to start collecting the data.
            - Classifications are computed based on observations.
            - For example, observations that were created for every news article tagged by people.

        JSON_OBJECT PARAMS:
            model           : name of the model. (required)
            subject_bucket  : bucket name for the subject observations that needs to be classified. (required)
            predicate       : `predicate` name for the subject observations that needs to be classified. (required)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_classifier({"model":"tagged_articles", "subject_bucket":"people", "predicate":"tags"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/classifier/init", json_request)

    def service_classifier_train(self, json_request={}):
        u"""/service/classifier/train : Trains a specific classifier model.

        NOTES:
            - Trainning means reading new observations linked to a model, and using them to extend the model.
            - Documents associated with the observation subjects are used for the classification.
            - More specifically, the fields (i.e. features) listed in the request.

        JSON_OBJECT PARAMS:
            model       : name of the classifier model. (required)
            features    : list of document features to use in the training. (required)
            options->use_numbers_as_weights : if set to True, causes the numeric weights to be applied (optional)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_classifier_train({"model":"tagged_articles", "features":["title","source"]})

            Or, if you want to use the observation values as weights.

            response = sqlrc.service_classifier_train({"model":"tagged_articles", "features":["title","source"], "options":{"use_numbers_as_weights":True}})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/classifier/train", json_request)

    def service_classifier_clear(self, json_request={}):
        u"""/service/classifier/clear : Removes all training data from a given classifier.

        NOTES:
            [TBD - Yet To Be Documented]

        JSON_OBJECT PARAMS:
            model   : name of the model to clear

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_classifier_clear({"model":"tagged_articles"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/classifier/clear", json_request)

    def service_classifier_reset(self, json_request={}):
        u"""/service/classifier/reset : Deletes ALL classification models in the database.

        NOTES:
            - This is a very damaging call so it requires a lot of caution (So, have CAUTION!!!)

        JSON_OBJECT PARAMS:
            none

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_classifier_reset({})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/classifier/reset", json_request)

    def service_classifier_predict(self, json_request={}):
        u"""/service/classifier/predict : Predicts the best classification label for a given document in a given model.

        NOTES:
            - It returns a label, a score and the score's ratio (i.e. that score's piece of the whole pie of labels).
            - If a specific label is not provided to be researched, the best label is returned.

        JSON_OBJECT PARAMS:
            model       : name of the model. (required)
            subject_id  : subject in the model that will be the context for the classification. (required)
            document    : new document to be classified. (required)
            label       : specific label to be queried (optional)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")

            # Returns best classification prediction (label)

            response = sqlrc.service_classifier_predict({"model":"tagged_articles", "subject_id":"003", "document":{"title":"OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}})
            # {u'_score': 26.426909, u'_ratio': 81.469171, u'label': u'AI'}

            # Returns classification prediction for a given label

            response = sqlrc.service_classifier_predict({"model":"tagged_articles", "subject_id":"001", "label":"Innovation", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}})
            # {u'_score': 4.774199, u'_ratio': 14.717953, u'label': u'Innovation'}


        RESPONSE:

            [TBD - Yet To Be Documented]
            # TODO: document when the response field are of type 'None'

        """
        return self._handler("/service/classifier/predict", json_request)

    def service_classifier_predictions(self, json_request={}):
        u"""/service/classifier/predictions : Returns all classification scores for all labels for a given subject.

        NOTES:
            - The response is a sorted list of labels and scores that best classify a document for a given subject.

        JSON_OBJECT PARAMS:
            model       : name of the model. (required)
            subject_id  : subject in the model that will be the context for the classification. (required)
            document    : new document to be classified. (required)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.service_classifier_predictions({"model":"tagged_articles", "subject_id":"001", "document":{"title":"Research Center OpenAI, will be established as a nonprofit, and will be based in San Francisco", "source":"techcrunch"}})

            # [{u'_score': 26.426909, u'_ratio': 81.469171, u'label': u'AI'}, {u'_score': 4.774199, u'_ratio': 14.717953, u'label': u'Innovation'}, {u'_score': 0.440237, u'_ratio': 1.357167, u'label': u'Tech'}, {u'_score': 0.2, u'_ratio': 0.616562, u'label': u'Politics'}, {u'_score': 0.158974, u'_ratio': 0.490088, u'label': u'Google'}, {u'_score': 0.158974, u'_ratio': 0.490088, u'label': u'Science'}, {u'_score': 0.105983, u'_ratio': 0.326725, u'label': u'Gaming'}, {u'_score': 0.105983, u'_ratio': 0.326725, u'label': u'Games'}, {u'_score': 0.066667, u'_ratio': 0.205521, u'label': u'Global Warming'}]

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/classifier/predictions", json_request)

    #
    # Recommendation
    #


    def service_recommend(self, json_request={}):
        u"""/service/collaborative/recommendation : Recommends subjects for an object, or objects for a subject.

        NOTES:
            - The recommendations are based on the relationships recorded in the observations.
            - Two computing metrics are available: pearson and manhattan
            - You have to provide either a subject_id or an object_id. The one left out is going to be recommended.

        JSON_OBJECT PARAMS:
            subject_bucket  : (required)
            subject_id      : (require only if an object_id is not provided)
            predicate       : predicate of the observations to be analyzed.
            object_bucket   : (required)
            object_id       : (required only if a subject_id is not provided)
            metric          : metric to use: pearson, or manhattan (optional, defaults to pearson)


        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")

            # recommendations based on object_ids "liked" by all subject_ids
            # what object_id should be recommended for this subject_id next? - pearson example

            response = sqlrc.service_recommend({"subject_bucket":"candidates", "subject_id":"001", "predicate":"likes", "object_bucket":"jobs"})
            # [{'bucket_id': 'jobs', '_score': 3.0, 'document_id': 'Python Engineer'}, {'bucket_id': 'jobs', '_score': 0.0, 'document_id': 'Java Engineer II'}]


            # recommendations based on subject_ids "who liked" these object_ids
            # what subject_id should be recommended for this object_id next - manhattan example

            response = sqlrc.service_recommend({"subject_bucket":"candidates", "predicate":"likes", "object_bucket":"jobs", "object_id":"Java Software Engineer", "metric":"manhattan"})
            # [{'bucket_id': 'candidates', '_score': 1.125, 'document_id': '009'}]


        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/collaborative/recommendation", json_request)

    def service_similarity(self, json_request={}):
        u"""/service/collaborative/similarity : Finds similar subjects for a subject, or similar objects for an object.

        NOTES:
            - The similarities are based on the relationships recorded in the observations.
            - Two computing metrics are available: pearson and manhattan
            - You have to provide either a subject_id or an object_id.

        JSON_OBJECT PARAMS:
            subject_bucket  : (required)
            subject_id      : (require only if an object_id is not provided)
            predicate       : predicate of the observations to be analyzed.
            object_bucket   : (required)
            object_id       : (required only if a subject_id is not provided)
            metric          : metric to use: pearson, or manhattan (optional, defaults to pearson)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")

            # finds subject_ids that are similar to this subject_id in terms of "liking" these "objects"

            response = sqlrc.service_similarity({"subject_bucket":"candidates", "subject_id":"001", "predicate":"likes", "object_bucket":"jobs", "method":"manhattan"})
            # [{u'bucket_id': u'candidates', u'num': 6, u'_score': 0.03288, u'document_id': u'003'}, {u'bucket_id': u'candidates', u'num': 1, u'_score': 0.0, u'document_id': u'009'}]


            # finds object_ids that are similar to this object_id in terms of being "liked" by these "subjects"

            response = sqlrc.service_similarity({"subject_bucket":"candidates", "predicate":"likes", "object_bucket":"jobs", "object_id":"MySQL DBA", "method":"pearson"})
            #[{u'bucket_id': u'jobs', u'num': 3, u'_score': 0.944911, u'document_id': u'Data Scientist'}, {u'bucket_id': u'jobs', u'num': 3, u'_score': 0.0, u'document_id': u'Oracle DBA'}, {u'bucket_id': u'jobs', u'num': 1, u'_score': 0.0, u'document_id': u'MySQL SysAdmin'}]

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/service/collaborative/similarity", json_request)

    #
    # Summarization
    #

    def service_summarization(self, json_request={}):
        u"""/service/summarization : Summarizes a document or document snippet, identifying keywords and entities.

        NOTES:
            [TBD - Yet To Be Documented]

        JSON_OBJECT PARAMS:
            bucket                          : document bucket (only required if a list of document ids is provided)
            documents                       : list with one ore more documents to be summarized.
                                              the documents are either inline objects or string identifiers.
            options -> max_sentences        : (optional, defaults to 10)
            options -> max_summary_size     : (optional, defaults to 6000)
            options -> max_summary_percent  : (optional, defaults to 80)
            options -> fields_to_summarize  : list of document fields to use in the summarization. (optional, defaults to ALL)
            options -> max_keywords         : max number of top keywords to return for each field (optional, defaults to 5)
            options -> max_entities         : max number of entities to extract  (optional, defaults to 10)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")

            # Summarizing an inline document

            response = sqlrc.service_summarization({"documents":[{"title":"Google To Launch An Artificial Intelligence Messenger Service To Rival Facebook M: Reports","summary":"According to sources close to the Wall Street Journal, Google is looking into launching a new mobile based messenger service underpinned by artificial intelligence. “For its new service, Google, a unit of Alphabet Inc., plans to integrate chatbots, software programs that answer questions inside a messaging app,” the article claims. Further sources have indicated that Nick Fox, currently vice president of communications at Google, has been leading a team for over a year to develop this new service."},{"title":"Google’s new messaging app to have artificial intelligence","summary":"Google is going to give a twist to normal messaging apps by coming up with a new one that employs artificial intelligence. The technology will bring Google’s data smarts to a chat bot service in the software. The new chat service will be an interesting feature allowing users to talk with friends or ask question of the chat bot. In return, the chat bot will look for answers from the search engine giant’s vast map of the internet."}], "options":{"max_sentences":1}})

            # {u'fields': {u'title': [[u'Google To Launch An Artificial Intelligence Messenger Service To Rival Facebook M: Reports', 54.0]], u'summary': [[u'For its new service, Google, a unit of Alphabet Inc., plans to integrate chatbots, software programs that answer questions inside a messaging app," the article claims. Further sources have indicated that Nick Fox, currently vice president of communications at Google, has been leading a team for over a year to develop this new service.', 115.45085]]}, u'field_entities': {u'title': [u'Reports', u'Google'], u'summary': [u'Google', u'Wall Street Journal', u'Nick Fox', u'Alphabet Inc']}, u'field_keywords': {u'title': [u'artificial intelligence', u'google', u'reports', u'service', u'launch'], u'summary': [u'chat bot', u'google', u'service', u'artificial intelligence', u'sources']}}

            # Summarizing a document from the database

            response = sqlrc.service_summarization({"bucket":"resumes", "documents":["001"], "options":{"max_keywords":10, "max_entities":5, "fields_to_summarize":["resume"]}})

            # Summarizing multiple documents from the database

            response = sqlrc.service_summarization({"bucket":"news", "documents":["002", "003"], "options":{"max_keywords":10, "max_entities":5, "fields_to_summarize":["news"]}})

        RESPONSE:

            [TBD - Yet To Be Documented]
            TODO: document field_entities, field_keywords

        """
        return self._handler("/service/summarization", json_request)

    #
    # Caching
    #

    def caching_initialize(self, json_request={}):
        u"""/caching/initialize : Initializes a caching structure

        NOTES:
            - This was originally designed as a Thread safe cache class.
            - Caching is eventually consistent, if flushed to the database.
            - The application itself uses some internal caching structures (e.g. _STOPWORDS)

        JSON_OBJECT PARAMS:
            bucket      : name to assign to the caching bucket.
            capacity    : max number of entries to store in this cache.
            auto_flush  : if True, automatically flushes the cache to the database.

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_initialize({"bucket":"stopwords", "capacity":"300", "auto_flush":False})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/caching/initialize", json_request)

    def caching_add(self, json_request={}):
        u"""/caching/add : Adds a key entry to an existing cache structure.

        NOTES:
            - This is essentially a shortcut to the /caching/put service, caching just the key.

        JSON_OBJECT PARAMS:
            bucket      : name of the caching bucket to use
            key         : key to cache
            expires_at  : number of seconds to keep this key in the cache

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_add({"bucket":"countries", "key":"canada"})

            # Set key that expires in 30 seconds
            response = sqlrc.caching_add({"bucket":"online_users", "key":"3432", "expires_at":30})

        RESPONSE:

            [TBD - Yet To Be Documented]
            # {
            #     "success": True
            # }

        """
        return self._handler("/caching/add", json_request)

    def caching_put(self, json_request={}):
        u"""/caching/put : Adds a key/value pair to an existing cache structure.

        NOTES:
            - A key can be removed, by forcing it to expire.

        JSON_OBJECT PARAMS:
            bucket      : name of the caching bucket to use
            key         : key to cache
            value       : value to cache
            expires_at  : number of seconds to keep this key in the cache

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_put("bucket":"stopwords", "key":"the", "value":True, "expires_at":10})

            # For a key expiration by setting its expires_at to a negative number.
            response = sqlrc.caching_put("bucket":"stopwords", "key":"the", "value":True, "expires_at":-1})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/caching/put", json_request)

    def caching_get(self, json_request={}):
        u"""/caching/get : Returns the value of a cached key

        NOTES:
            - If a key doesn't exist, it should return a value of None.
            - Trying to access an empty cache should return an error.

        JSON_OBJECT PARAMS:
            bucket  : Cache bucket to query.
            key     : Key being queried.


        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_get({"bucket":"stopwords", "key":"the"})

        RESPONSE:

            [TBD - Yet To Be Documented]
            # {
            #     "success" : True,
            #     "key" : "the",
            #     "value" : True
            # }

        """
        return self._handler("/caching/get", json_request)

    def caching_remove(self, json_request={}):
        u"""/caching/remove : Removes a key from a cache.

        NOTES:
            [TBD - Yet To Be Documented]

        JSON_OBJECT PARAMS:
            bucket  : caching bucket that contains the key to be deleted
            key     : key to be deleted (optional, if not provided, all keys in the bucket are deleted)

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_remove({"bucket":"_STOPWORDS", "key":"the"})

            # Deleting all keys
            response = sqlrc.caching_remove({"bucket":"_STOPWORDS"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/caching/remove", json_request)

    def caching_flush(self, json_request={}):
        u"""/caching/flush : Persists cache in-memory data changes to the database.

        NOTES:
            [TBD - Yet To Be Documented]

        JSON_OBJECT PARAMS:
            bucket  : caching bucket to flush to the database

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_flush({"bucket":"stopwords"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/caching/flush", json_request)

    def caching_reset(self, json_request={}):
        u"""/caching/reset : Deletes ALL non-system caches in the database.

        NOTES:
            - This is a very damaging call so it requires a lot of caution (So, have CAUTION!!!)

        JSON_OBJECT PARAMS:
            none

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_reset({})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/caching/reset", json_request)

    def caching_destroy(self, json_request={}):
        u"""/caching/destroy : Destroys the entire caching object.

        NOTES:
            [TBD - Yet To Be Documented]

        JSON_OBJECT PARAMS:
            bucket  : name of the bucket to be destroyed.

        EXAMPLE REQUEST:

            import sqlpie_client
            sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
            response = sqlrc.caching_destroy({"bucket":"stopwords"})

        RESPONSE:

            [TBD - Yet To Be Documented]

        """
        return self._handler("/caching/destroy", json_request)
