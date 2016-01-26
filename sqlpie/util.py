# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import hashlib
import uuid
from datetime import datetime
import base64
import zlib
import os
from dateutil.parser import *
import time

class Util(object):

    @staticmethod
    def to_sha1(value, hexdigest=True):
        """
        creates a unique identifier for a user-created 'id'
        """
        hash_object = hashlib.sha1(value)
        if hexdigest:
            ret = hash_object.hexdigest()
        else:
            ret = hash_object.digest()
        return ret

    @staticmethod
    def get_unique_identifier():
        """
        creates a unique identifier for the document, if one hasn't been provided by the user.
        """
        ret = uuid.uuid1().hex
        return ret

    @staticmethod
    def get_current_utc_timestamp():
        return datetime.utcnow()

    @staticmethod
    def get_current_utc_from_timestamp(seconds_since_epoch):
        return datetime.fromtimestamp(int(seconds_since_epoch))

    @staticmethod
    def compress(original):
        """
        encode and compress the json document
        """
        return original.encode('zlib').encode('base64')

    @staticmethod
    def uncompress(encoded):
        """
        uncompress and decode the json document
        """
        return encoded.decode('base64').decode('zlib')

    @staticmethod
    def is_debug():
        is_debug = os.environ.get('sqlpie_debug', False)
        return str(is_debug).lower() == "true"

    @staticmethod
    def is_number(input):
        if Util.is_float(input) or Util.is_int(input):
            return True
        else:
            return False

    @staticmethod
    def is_float(input):
      try:
        num = float(input)
      except ValueError:
        return False
      return True

    @staticmethod
    def is_int(input):
      try:
        num = int(input)
      except ValueError:
        return False
      return True

    @staticmethod
    def json_unicode_to_bytes(json_data):
        json_bytes = json_data
        if isinstance(json_data, unicode) or isinstance(json_data, basestring):
            json_bytes = json_data.encode('utf-8').replace('"','\\"')
        elif isinstance(json_data, dict):
            json_bytes = {Util.json_unicode_to_bytes(k):Util.json_unicode_to_bytes(v) for k,v in json_data.iteritems()}
        elif isinstance(json_data, list):
            json_bytes = [Util.json_unicode_to_bytes(element) for element in json_data]
        elif isinstance(json_data, tuple):
            json_bytes = Util.json_unicode_to_bytes(list(json_data))
        return json_bytes

    @staticmethod
    def convert_to_date(value):
        try:
            datedefault = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            datetime_obj = parse(value, default=datedefault)
            return time.mktime(datetime_obj.timetuple())
        except:
            pass
        return False


def walk(d, is_list=False, ancestors="", pairs=[], init=True):
    """
    transverses a json document and returns a list of keys and types.
    """
    if init:
        is_list, ancestors, pairs = False, "", []

    if not is_list:
        for k, v in d.iteritems():
            if isinstance(v, dict):
                k = k + "." + ancestors
                pairs = walk(v, False, k, pairs, False)
            elif isinstance(v, list):
                k = k + "." + ancestors
                pairs = walk(v, True, k, pairs, False)
            else:
                k = k + "." + ancestors
                pairs.append((type(v).__name__, k, unicode(v)))
    else:
        for v in d:
            if isinstance(v, dict):
                pairs = walk(v, False, ancestors, pairs, False)
            elif isinstance(v, list):
                pairs = walk(v, True, ancestors, pairs, False)
            else:
                k = ancestors
                pairs.append((type(v).__name__, k, unicode(v)))
    return pairs
