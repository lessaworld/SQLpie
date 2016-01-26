# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import sqlpie_client

sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000", json_responses=False)

response = sqlrc.document_remove({"_bucket":"test_products", "_id":"00032"})
print "Let's ensure that our test product is not in the test_products bucket."
print response
print

response = sqlrc.document_get({"_id":"00032", "_bucket":"test_products"})
print "This should not find the document."
print response
print

response = sqlrc.document_put({"documents":{"_id":"00032", "_bucket":"test_products", "product":"Hello World Laptop Computer", "price":23.50}})
print "So now it's time to add a new document."
print response
print

response = sqlrc.document_get({"_id":"00032", "_bucket":"test_products"})
print "The document can now be retrieved."
print response
print