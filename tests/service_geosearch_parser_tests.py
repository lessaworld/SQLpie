# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class ServiceGeoSearchParserTests(object):
    #
    # Service Geo Search Tests
    #

    def run_before_service_geosearch_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        employees = {"documents":[{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA","title":"CEO"},{"_id":"002", "_bucket":"employees","name":"Peter","location":"Cleveland, OH","title":"CFO"},{"_id":"003", "_bucket":"employees","name":"Jeff","location":"Wexford, PA", 'title': "Team Lead"},{"_id":"004", "_bucket":"employees","name":"Beth","location":"Los Angeles, CA"},{"_id":"005", "_bucket":"employees","name":"Jack","location":"Bethel Park, PA","title":"Chief Marketing Officer"},{"_id":"006", "_bucket":"employees","name":"Mike","location":"Monroeville, PA"},{"_id":"007", "_bucket":"employees","name":"Nancy","location":"Chicago, IL", 'title': "Software Engineer"},{"_id":"008", "_bucket":"employees","name":"Anne","location":"Philadelphia, PA","title":"COO"}], "options":{"parsers":["sample"]}}
        response = self.app.post('/document/put', data=json.dumps(employees), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def run_before_service_geosearch_no_parser_tests(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        employees = {"documents":[{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA", "latitude":40.4405556, "longitude":-79.9961111,"title":"CEO"},{"_id":"002", "_bucket":"employees","name":"Peter","location":"Cleveland, OH","latitude":41.4994444, "longitude":-81.6955556,"title":"CFO"},{"_id":"003", "_bucket":"employees","name":"Jeff","location":"Wexford, PA","latitude":40.6263889, "longitude":-80.0561111, 'title': "Team Lead"},{"_id":"004", "_bucket":"employees","name":"Beth","location":"Los Angeles, CA","latitude":34.0522222, "longitude":-118.2427778},{"_id":"005", "_bucket":"employees","name":"Jack","location":"Bethel Park, PA","latitude":40.3275000, "longitude":-80.0397222,"title":"Chief Marketing Officer"},{"_id":"006", "_bucket":"employees","name":"Mike","location":"Monroeville, PA","latitude":40.4211111, "longitude":-79.7883333},{"_id":"007", "_bucket":"employees","name":"Nancy","location":"Chicago, IL","latitude":41.8500000, "longitude":-87.6500000, 'title': "Software Engineer"},{"_id":"008", "_bucket":"employees","name":"Anne","location":"Philadelphia, PA","latitude":39.9522222, "longitude":-75.1641667,"title":"COO"}]}
        response = self.app.post('/document/put', data=json.dumps(employees), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def run_before_service_geosearch_no_geo_info(self):
        response = self.app.post('/document/reset', data=json.dumps({}), content_type = 'application/json')

        employees = {"documents":[{"_id":"001", "_bucket":"employees","name":"John","location":"Pittsburgh, PA","title":"CEO"},{"_id":"002", "_bucket":"employees","name":"Peter","location":"Cleveland, OH","title":"CFO"},{"_id":"003", "_bucket":"employees","name":"Jeff","location":"Wexford, PA", 'title': "Team Lead"},{"_id":"004", "_bucket":"employees","name":"Beth","location":"Los Angeles, CA"},{"_id":"005", "_bucket":"employees","name":"Jack","location":"Bethel Park, PA","title":"Chief Marketing Officer"},{"_id":"006", "_bucket":"employees","name":"Mike","location":"Monroeville, PA"},{"_id":"007", "_bucket":"employees","name":"Nancy","location":"Chicago, IL", 'title': "Software Engineer"},{"_id":"008", "_bucket":"employees","name":"Anne","location":"Philadelphia, PA","title":"COO"}]}
        response = self.app.post('/document/put', data=json.dumps(employees), content_type = 'application/json')
        response = self.app.post('/service/index', data=json.dumps({"options":{"rebuild":True}}), content_type = 'application/json')

    def test_service_geosearch_01_radius_all(self):
        self.run_before_service_geosearch_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"_bucket:employees","georadius":20,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'name': u'Jeff', u'title': u'Team Lead', u'_score': 1.018417, u'longitude': -80.0561111, u'_bucket': u'employees', u'location': u'Wexford, PA', u'_distance': 13.221567, u'latitude': 40.6263889, u'_id': u'003'}, {u'name': u'Mike', u'_score': 1.067171, u'longitude': -79.7883333, u'_bucket': u'employees', u'location': u'Monroeville, PA', u'_distance': 11.010648, u'latitude': 40.4211111, u'_id': u'006'}, {u'name': u'Jack', u'title': u'Chief Marketing Officer', u'_score': 1.023527, u'_distance': 8.142142, u'longitude': -80.0397222, u'_bucket': u'employees', u'location': u'Bethel Park, PA', u'is_c_level': True, u'latitude': 40.3275, u'_id': u'005'}, {u'name': u'John', u'title': u'CEO', u'_score': 1.084029, u'_distance': 0.0, u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'is_c_level': True, u'latitude': 40.4405556, u'_id': u'001'}], "Actual Response : %r" % json_response

    def test_service_geosearch_02_radius_and_field_target(self):
        self.run_before_service_geosearch_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"PA _bucket:employees","georadius":20,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'name': u'Jeff', u'title': u'Team Lead', u'_score': 0.178765, u'longitude': -80.0561111, u'_bucket': u'employees', u'location': u'Wexford, PA', u'_distance': 13.221567, u'latitude': 40.6263889, u'_id': u'003'}, {u'name': u'Mike', u'_score': 0.210746, u'longitude': -79.7883333, u'_bucket': u'employees', u'location': u'Monroeville, PA', u'_distance': 11.010648, u'latitude': 40.4211111, u'_id': u'006'}, {u'name': u'Jack', u'title': u'Chief Marketing Officer', u'_score': 0.155425, u'_distance': 8.142142, u'longitude': -80.0397222, u'_bucket': u'employees', u'location': u'Bethel Park, PA', u'is_c_level': True, u'latitude': 40.3275, u'_id': u'005'}, {u'name': u'John', u'title': u'CEO', u'_score': 0.188209, u'_distance': 0.0, u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'is_c_level': True, u'latitude': 40.4405556, u'_id': u'001'}], "Actual Response : %r" % json_response

    def test_service_geosearch_03_radius_and_latlong_target(self):
        self.run_before_service_geosearch_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","georadius":1,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')
        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response

    def test_service_geosearch_04_radius_without_target(self):
        self.run_before_service_geosearch_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","georadius":20}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert "Bad Request. Invalid Arguments." in json_response["err"], "Actual Response : %r" % json_response

    def test_service_geosearch_05_target_without_radius(self):
        self.run_before_service_geosearch_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert "Bad Request. Invalid Arguments." in json_response["err"], "Actual Response : %r" % json_response

    def test_service_geosearch_06_missing_geo_data(self):
        self.run_before_service_geosearch_no_geo_info()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","georadius":20,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 0, "Actual Response : %r" % json_response

    def test_service_geosearch_07_radius_all(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"_bucket:employees","georadius":20,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'name': u'Jeff', u'title': u'Team Lead', u'_score': 1.018417, u'longitude': -80.0561111, u'_bucket': u'employees', u'location': u'Wexford, PA', u'_distance': 13.221567, u'latitude': 40.6263889, u'_id': u'003'}, {u'name': u'Mike', u'_score': 1.067171, u'longitude': -79.7883333, u'_bucket': u'employees', u'location': u'Monroeville, PA', u'_distance': 11.010648, u'latitude': 40.4211111, u'_id': u'006'}, {u'name': u'Jack', u'title': u'Chief Marketing Officer', u'_score': 0.990639, u'longitude': -80.0397222, u'_bucket': u'employees', u'location': u'Bethel Park, PA', u'_distance': 8.142142, u'latitude': 40.3275, u'_id': u'005'}, {u'name': u'John', u'title': u'CEO', u'_score': 1.038921, u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'_distance': 0.0, u'latitude': 40.4405556, u'_id': u'001'}], "Actual Response : %r" % json_response

    def test_service_geosearch_08_radius_and_field_target(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"PA _bucket:employees","georadius":20,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'name': u'Jeff', u'title': u'Team Lead', u'_score': 0.178765, u'longitude': -80.0561111, u'_bucket': u'employees', u'location': u'Wexford, PA', u'_distance': 13.221567, u'latitude': 40.6263889, u'_id': u'003'}, {u'name': u'Mike', u'_score': 0.210746, u'longitude': -79.7883333, u'_bucket': u'employees', u'location': u'Monroeville, PA', u'_distance': 11.010648, u'latitude': 40.4211111, u'_id': u'006'}, {u'name': u'Jack', u'title': u'Chief Marketing Officer', u'_score': 0.157977, u'longitude': -80.0397222, u'_bucket': u'employees', u'location': u'Bethel Park, PA', u'_distance': 8.142142, u'latitude': 40.3275, u'_id': u'005'}, {u'name': u'John', u'title': u'CEO', u'_score': 0.192794, u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'_distance': 0.0, u'latitude': 40.4405556, u'_id': u'001'}], "Actual Response : %r" % json_response

    def test_service_geosearch_09_radius_and_latlong_target(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","georadius":1,"geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response

    def test_service_geosearch_10_radius_without_target(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","georadius":20}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert "Bad Request. Invalid Arguments." in json_response["err"], "Actual Response : %r" % json_response

    def test_service_geosearch_11_target_without_radius(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees","geotarget":"40.4405556,-79.9961111"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == False, "Actual Response : %r" % json_response
        assert "Bad Request. Invalid Arguments." in json_response["err"], "Actual Response : %r" % json_response

    def test_service_geosearch_12_radius_all_sort_by_relevance(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"_bucket:employees", "georadius":20, "geotarget":"40.4405556,-79.9961111","geosortby":"relevance"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'name': u'Mike', u'_score': 1.067171, u'longitude': -79.7883333, u'_bucket': u'employees', u'location': u'Monroeville, PA', u'_distance': 11.010648, u'latitude': 40.4211111, u'_id': u'006'}, {u'name': u'John', u'title': u'CEO', u'_score': 1.038921, u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'_distance': 0.0, u'latitude': 40.4405556, u'_id': u'001'}, {u'name': u'Jeff', u'title': u'Team Lead', u'_score': 1.018417, u'longitude': -80.0561111, u'_bucket': u'employees', u'location': u'Wexford, PA', u'_distance': 13.221567, u'latitude': 40.6263889, u'_id': u'003'}, {u'name': u'Jack', u'title': u'Chief Marketing Officer', u'_score': 0.990639, u'longitude': -80.0397222, u'_bucket': u'employees', u'location': u'Bethel Park, PA', u'_distance': 8.142142, u'latitude': 40.3275, u'_id': u'005'}], "Actual Response : %r" % json_response

    def test_service_geosearch_13_radius_and_field_target_sort_by_relevance(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"PA _bucket:employees", "georadius":20, "geotarget":"40.4405556,-79.9961111", "geosortby":"relevance"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert json_response["results"]["documents"] == [{u'name': u'Mike', u'_score': 0.210746, u'longitude': -79.7883333, u'_bucket': u'employees', u'location': u'Monroeville, PA', u'_distance': 11.010648, u'latitude': 40.4211111, u'_id': u'006'}, {u'name': u'John', u'title': u'CEO', u'_score': 0.192794, u'longitude': -79.9961111, u'_bucket': u'employees', u'location': u'Pittsburgh, PA', u'_distance': 0.0, u'latitude': 40.4405556, u'_id': u'001'}, {u'name': u'Jeff', u'title': u'Team Lead', u'_score': 0.178765, u'longitude': -80.0561111, u'_bucket': u'employees', u'location': u'Wexford, PA', u'_distance': 13.221567, u'latitude': 40.6263889, u'_id': u'003'}, {u'name': u'Jack', u'title': u'Chief Marketing Officer', u'_score': 0.157977, u'longitude': -80.0397222, u'_bucket': u'employees', u'location': u'Bethel Park, PA', u'_distance': 8.142142, u'latitude': 40.3275, u'_id': u'005'}], "Actual Response : %r" % json_response

    def test_service_geosearch_14_radius_and_latlong_target_sort_by_relevance(self):
        self.run_before_service_geosearch_no_parser_tests()

        response = self.app.post('/service/search', data=json.dumps({"q":"john _bucket:employees", "georadius":1, "geotarget":"40.4405556,-79.9961111","geosortby":"relevance"}), content_type = 'application/json')

        json_response = json.loads(response.data)
        assert json_response["success"] == True, "Actual Response : %r" % json_response
        assert len(json_response["results"]["documents"]) == 1, "Actual Response : %r" % json_response