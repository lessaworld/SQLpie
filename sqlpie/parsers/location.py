# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

def parse(d=None):

    #
    # TO DO : Add an lat/long look up here based on location and zip code.
    #
    if d is not None:
        d["latitude"] = 0
        d["longitude"] = 0
    return d or {}

if __name__ == "__main__":
    #
    # Testing & Debugging
    #
    sample_doc = {'_id': '001', 'name': 'John', '_bucket': 'employees', 'location': 'Pittsburgh, PA'}
    print parse(sample_doc)
