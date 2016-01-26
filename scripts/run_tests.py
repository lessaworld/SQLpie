# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import os
os.environ["sqlpie_env"] = "test"

import sys
sys.path.append(os.getcwd())

from flask import Flask, current_app, g
from flask import jsonify
from flaskext.mysql import MySQL
import application

import unittest
import json
import sys, traceback
import sqlpie
import tests

class ApplicationTestCase(unittest.TestCase, tests.DocumentTests, tests.ObservationTests, \
    tests.ServiceIndexerTests, tests.ServiceSearcherTests, tests.HealthTests, \
    tests.UtilTests, tests.CachingTests, tests.ServiceTagCloudTests, tests.ServiceGeoSearchParserTests, \
    tests.ServiceClassifierTests, tests.ServiceMatchingTests, tests.ServiceCollaborativeTests, \
    tests.ServiceSummarizationTests):

    def setUp(self):
        self.app = application.application.test_client()

    def tearDown(self):
        pass

if __name__ == '__main__':

    #
    # Reset All tables
    #

    app = Flask(__name__)
    with app.app_context():
        setup = sqlpie.DBSetup(sqlpie.Config().load())
        setup.init(current_app)
        mysql = setup.db()

        try:
            g.conn = mysql.connect()
            g.cursor = g.conn.cursor()
            g.conn.begin()

            sqlpie.DBSetup(sqlpie.Config().load()).reset_database()

            g.conn.commit()
        except Exception as e:
            print "\n[Error] Can't connect to the database.\n"
            if sqlpie.Util.is_debug():
                traceback.print_tb(sys.exc_info()[2])
            try:
                g.conn.rollback()
            except:
                pass
        finally:
            try:
                g.cursor.close()
                g.conn.close()
            except:
                exit()

    #
    # Run tests
    #

    unittest.main()
