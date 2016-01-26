# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class CachingTests(object):

    #
    # Caching methods Tests
    #

    def test_service_caching_auto_flush_false(self):

        # Initialize Cache

        request = {"bucket":"stopwords", "capacity":"300", "auto_flush":False}
        response = self.app.post('/caching/initialize', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Set key that expires in 10 seconds

        request = {"bucket":"stopwords", "key":"the", "value":True, "expires_at":10}
        response = self.app.post('/caching/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Get a key

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Set key to expire in -10 seconds

        request = {"bucket":"stopwords", "key":"so", "value":True, "expires_at":-10}
        response = self.app.post('/caching/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Try to get the key. It should return nothing.

        request = {"bucket":"stopwords", "key":"so"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["key"] == "so", "Actual Response : %r" % json_response
        assert json_response["value"] is None, "Actual Response : %r" % json_response

        # Delete a previously-stored key

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/remove', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Try to get deleted (non-existent) key

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["key"] == "the", "Actual Response : %r" % json_response
        assert json_response["value"] is None, "Actual Response : %r" % json_response


        # Flush cache's in-memory data to DB

        request = {"bucket":"stopwords"}
        response = self.app.post('/caching/flush', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Delete all DB data for the given cache

        request = {"bucket":"stopwords"}
        response = self.app.post('/caching/remove', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Destroy Cache Object

        request = {"bucket":"stopwords"}
        response = self.app.post('/caching/destroy', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Try to access empty cache

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert json_response["err"] == sqlpie.CustomException.CACHE_IS_EMPTY, "Actual Response : %r" % json_response

    def test_service_caching_auto_flush_true(self):

        # Initialize Cache

        request = {"bucket":"stopwords", "capacity":"300", "auto_flush":True}
        response = self.app.post('/caching/initialize', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Set key that expires in 10 seconds

        request = {"bucket":"stopwords", "key":"the", "expires_at":10}
        response = self.app.post('/caching/add', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Set key that expires in 10 seconds

        request = {"bucket":"stopwords", "key":"the", "value":True, "expires_at":10}
        response = self.app.post('/caching/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Get a key

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Set key to expire in -10 seconds

        request = {"bucket":"stopwords", "key":"so", "value":True, "expires_at":-10}
        response = self.app.post('/caching/put', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Try to get the key. It should return nothing.

        request = {"bucket":"stopwords", "key":"so"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True    , "Actual Response : %r" % json_response
        assert json_response["key"] == "so", "Actual Response : %r" % json_response
        assert json_response["value"] is None, "Actual Response : %r" % json_response

        # Delete a previously-stored key

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/remove', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Try to get deleted key

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["key"] == "the", "Actual Response : %r" % json_response
        assert json_response["value"] is None, "Actual Response : %r" % json_response

        # Flush cache's in-memory data to DB

        request = {"bucket":"stopwords"}
        response = self.app.post('/caching/flush', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Delete all DB data for the given cache

        request = {"bucket":"stopwords"}
        response = self.app.post('/caching/remove', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Destroy Cache Object

        request = {"bucket":"stopwords"}
        response = self.app.post('/caching/destroy', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response

        # Try to access empty cache

        request = {"bucket":"stopwords", "key":"the"}
        response = self.app.post('/caching/get', data=json.dumps(request), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert json_response["err"] == sqlpie.CustomException.CACHE_IS_EMPTY, "Actual Response : %r" % json_response
