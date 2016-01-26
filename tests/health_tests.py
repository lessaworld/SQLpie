# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class HealthTests(object):

    #
    # Health Tests
    #

    def test_ping(self):
        response = self.app.get('/ping')
        assert 'pong' in response.data, "Actual Response : %r" % json_response
