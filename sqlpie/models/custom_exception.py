# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

class CustomException(Exception):
    RECORD_NOT_FOUND = "Record Not Found."
    INVALID_ARGUMENTS = "Bad Request. Invalid Arguments."
    CACHE_IS_EMPTY = "Cache Is Empty."
    CACHE_KEY_NOT_FOUND = "Cache Key Not Found."
    INVALID_STOPWORD_FILE = "Invalid Stopword File."
    INVALID_PARSER = "Invalid Indexing Parser."
    INVALID_CONFIG_FILE_FORMAT = "Invalid Config File Format."