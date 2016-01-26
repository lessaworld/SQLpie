# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""
import re

def parse(d={}):
    if "location" in d:
        coords = {"pittsburgh, pa":[40.4405556,-79.9961111], "cleveland, oh":[41.4994444,-81.6955556], \
                      "wexford, pa":[40.6263889,-80.0561111], "los angeles, ca":[34.0522222,-118.2427778], \
                    "bethel park, pa":[40.3275000,-80.0397222], "monroeville, pa":[40.4211111,-79.7883333], \
                    "chicago, il":[41.8500000,-87.6500000], "philadelphia, pa":[39.9522222,-75.1641667]}
        l = d["location"].lower()
        if l in coords:
            geo_lat, geo_long = coords[l]
            d["latitude"] = geo_lat
            d["longitude"] = geo_long

    if "title" in d:
        l = d["title"].lower()
        if re.search(r"\bc[a-z]{2}\b", l) or re.search(r"Chief \b[a-z]*\b \b[a-z]*\b", l, re.IGNORECASE):
            d["is_c_level"] = True

    return d

if __name__ == "__main__":
    #
    # Testing & Debugging
    #
    sample_doc = {'_id': '001', 'name': 'John', '_bucket': 'employees', 'location': 'Pittsburgh, PA'}
    print parse(sample_doc)
    print
    sample_doc = {'_id': '002', 'name': 'John', '_bucket': 'employees', 'location': 'Cleveland, OH', 'title': 'CEO'}
    print parse(sample_doc)
    print
    sample_doc = {'_id': '002', 'name': 'John', '_bucket': 'employees', 'location': 'Cleveland, OH', 'title': 'Chief Operating Officer'}
    print parse(sample_doc)
    print
    sample_doc = {'_id': '002', 'name': 'John', '_bucket': 'employees', 'location': 'Cleveland, OH', 'title': 'Software Engineer'}
    print parse(sample_doc)
    print
