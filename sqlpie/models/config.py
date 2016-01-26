# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import sqlpie
import json, os

class Config(object):

    STOPWORDS = "_STOPWORDS"
    OPTIONS = "_OPTIONS"

    SERVER_PORT = "server.port"
    SEARCH_STOPWORDS = "search.stopwords"
    OUTPUT_JSON_BYTESTRINGS = "output.json_bytestrings"
    BACKGROUND_INDEXER = "background.indexer"

    @staticmethod
    def load():
        json_file = open(os.path.dirname(__file__) + '/../../config/config.json')
        json_str = json_file.read()
        try:
            c = json.loads(json_str)
        except:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_CONFIG_FILE_FORMAT)
        return c

    @staticmethod
    def load_data(filename):
        filename = os.path.dirname(__file__) + "/../data/"+filename
        try:
            with open(filename) as f:
                words = [line.strip('\n') for line in f]
        except IOError as e:
            raise sqlpie.CustomException(sqlpie.CustomException.INVALID_STOPWORD_FILE)
        return words

    @staticmethod
    def get(key):
        try:
            config = sqlpie.global_cache[sqlpie.Config.OPTIONS].get("options")[key]
        except KeyError:
            config = None
        return config
