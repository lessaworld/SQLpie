# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import sqlpie_client

sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000", json_responses=False)
response = sqlrc.ping()
print "this is a nicelly formatted text output:"
print response
print

# Returns plain text
#
# {
#     "ping": "pong"
# }


sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
response = sqlrc.ping()

print "this is a JSON (Python dictionary) object:"
print response
print
print "... and this the key being directly accessed."
print response["ping"]

# Returns a JSON object
# {u'ping': u'pong'}
# pong