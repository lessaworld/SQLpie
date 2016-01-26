# -*- coding: utf-8 -*-
"""

SQLpie™ is a simple, sleek, intuitive, and powerful API platform for prototyping projects that have data intelligence needs.

SQLpie is 100% written in Python and sits on top of a MySQL database, which means that it's easy to maintain and most (if not all) of the data processing heavy lifting is done in SQL, a proven and somewhat scalable technology.

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import Flask, request, jsonify, g, Response
from flask import current_app
from flask import render_template
from flaskext.mysql import MySQL
import json, threading, time, sys, traceback, os, logging, random
import sqlpie

application = Flask(__name__)

sqlpie_config = sqlpie.Config().load()
setup = sqlpie.DBSetup(sqlpie_config)
setup.init(application)
mysql = setup.db()

@application.before_request
def db_connect():
    try:
        g.conn = mysql.connect()
        g.cursor = g.conn.cursor()
    except:
        pass

@application.teardown_request
def db_disconnect(response):
    try:
        g.cursor.close()
        g.conn.close()
    except:
        pass
    return response

#
# Routes
#

@application.route('/')
def index():
    return 'Hello world, this is SQLpie.'

#
# Documents
#

@application.route("/document/<command>", methods=['POST'])
def document(command):
    command = command.lower()
    if command == "put":
        resp = sqlpie.DocumentController.put(request)
    elif command == "get":
        resp = sqlpie.DocumentController.get(request)
    elif command == "remove":
        resp = sqlpie.DocumentController.remove(request)
    elif command == "reset":
        resp = sqlpie.DocumentController.reset(request)
    else:
        resp = Response(None, status=404, mimetype='application/json')
    return resp

#
# Observations
#

@application.route("/observation/<command>", methods=['POST'])
def observation(command):
    command = command.lower()
    if command == "put":
        resp = sqlpie.ObservationController.put(request)
    elif command == "get":
        resp = sqlpie.ObservationController.get(request)
    elif command == "remove":
        resp = sqlpie.ObservationController.remove(request)
    elif command == "reset":
        resp = sqlpie.ObservationController.reset(request)
    else:
        resp = Response(None, status=404, mimetype='application/json')
    return resp

#
# Other
#

@application.route("/docs", methods=["GET"])
def docs():
    return sqlpie.HealthController.docs(request)

@application.route("/stats", methods=["GET","POST"])
def stats():
    return sqlpie.HealthController.stats(request)

@application.route("/ping", methods=["GET","POST"])
def ping():
    return sqlpie.HealthController.ping(request)

#
# Search
#

@application.route("/service/index", methods=["POST"])
def service_index():
    return sqlpie.SearchController.service_index(request)

@application.route("/service/search", methods=["POST"])
def service_search():
    return sqlpie.SearchController.service_search(request)

#
# Classifier
#

@application.route("/service/classifier/init", methods=["POST"])
def service_classifier():
    return sqlpie.ClassifierController.classifier_init(request)

@application.route("/service/classifier/train", methods=["POST"])
def service_classifier_train():
    return sqlpie.ClassifierController.classifier_train(request)

@application.route("/service/classifier/clear", methods=["POST"])
def service_classifier_clear():
    return sqlpie.ClassifierController.classifier_clear(request)

@application.route("/service/classifier/reset", methods=["POST"])
def service_classifier_reset():
    return sqlpie.ClassifierController.classifier_reset(request)

@application.route("/service/classifier/predict", methods=["POST"])
def service_classifier_predict():
    return sqlpie.ClassifierController.classifier_predict(request)

@application.route("/service/classifier/predictions", methods=["POST"])
def service_classifier_predictions():
    return sqlpie.ClassifierController.classifier_predictions(request)

#
# Matching
#

@application.route("/service/matching/", methods=["POST"])
def service_matching():
    return sqlpie.MatchingController.matching(request)

#
# Recommendation
#

@application.route("/service/collaborative/recommendation", methods=["POST"])
def service_recommend():
    return sqlpie.CollaborativeController.service_recommend(request)

@application.route("/service/collaborative/similarity", methods=["POST"])
def service_similarity():
    return sqlpie.CollaborativeController.service_similarity(request)

#
# Summarization
#

@application.route("/service/summarization", methods=["POST"])
def service_summarization():
    return sqlpie.SummarizationController.service_summarization(request)

#
# Caching
#

@application.route("/caching/initialize", methods=["POST"])
def caching_initialize():
    return sqlpie.CachingController.caching_initialize(request)

@application.route("/caching/add", methods=["POST"])
def caching_add():
    return sqlpie.CachingController.caching_add(request)

@application.route("/caching/put", methods=["POST"])
def caching_put():
    return sqlpie.CachingController.caching_put(request)

@application.route("/caching/get", methods=["POST"])
def caching_get():
    return sqlpie.CachingController.caching_get(request)

@application.route("/caching/remove", methods=["POST"])
def caching_remove():
    return sqlpie.CachingController.caching_remove(request)

@application.route("/caching/flush", methods=["POST"])
def caching_flush():
    return sqlpie.CachingController.caching_flush(request)

@application.route("/caching/reset", methods=["POST"])
def caching_reset():
    return sqlpie.CachingController.caching_reset(request)

@application.route("/caching/destroy", methods=["POST"])
def caching_destroy():
    return sqlpie.CachingController.caching_destroy(request)


#
# Global Vars
#

if "options" in sqlpie_config:
    options = sqlpie_config["options"]
    sqlpie.global_cache[sqlpie.Config.OPTIONS] = sqlpie.Caching(sqlpie.Config.OPTIONS,1)
    sqlpie.global_cache[sqlpie.Config.OPTIONS].put("options", options)

    search_stopwords = sqlpie.Config.get(sqlpie.Config.SEARCH_STOPWORDS)
    if search_stopwords is not None:
        sqlpie.global_cache[sqlpie.Config.STOPWORDS] = sqlpie.Caching(sqlpie.Config.STOPWORDS,5000)
        for stopword_file in search_stopwords:
            words = sqlpie.Config.load_data(stopword_file)
            for w in words:
                sqlpie.global_cache[sqlpie.Config.STOPWORDS].add(w.strip())

#
# Background Threads
#

def handle_indexing(app, mysql):
    with app.app_context():
        while(True):
            try:
                g.conn = mysql.connect()
                g.cursor = g.conn.cursor()
                g.conn.begin()
                # run indexing servie every 300 seconds
                time.sleep(300)
                sqlpie.Indexer().index_documents()
                g.conn.commit()
            except Exception as e:
                if sqlpie.Util.is_debug():
                    traceback.print_tb(sys.exc_info()[2])
                try:
                    g.conn.rollback()
                except:
                    pass
            finally:
                #  if the MySQL Server is not running, this will fail.
                try:
                    g.cursor.close()
                    g.conn.close()
                except:
                    pass

if sqlpie.DBSetup().environment() != "test":
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threads = []
        if sqlpie.Config.get(sqlpie.Config.BACKGROUND_INDEXER) == True:
            t = threading.Thread(name='handle_indexing', target=handle_indexing, args=(application, mysql))
            t.setDaemon(True)
            threads.append(t)
            t.start()

        # for t in threads:
        #     t.join()

if sqlpie.Util.is_debug():
    application.debug=True

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=sqlpie.Util.is_debug(), port=sqlpie.Config.get(sqlpie.Config.SERVER_PORT))
