# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import os

import sys, random
sys.path.append(os.getcwd())

from flask import Flask, current_app, g
from flask import jsonify
from flaskext.mysql import MySQL
import application

import sqlpie

if __name__ == '__main__':

    print "\nTo confirm you want to (re)create the sqlpie_%s database environment... " % sqlpie.DBSetup.environment()
    confirmation_code = random.randrange(100, 999)
    cmd = raw_input("... please solve the following equation: %s + 1 = " % confirmation_code)
    if cmd.isdigit() and int(cmd) == confirmation_code + 1:
        print "Ok. Setting up the database now...\n\n"

        application = Flask(__name__)
        with application.app_context():
            sqlpie.DBSetup.create_database(application, sqlpie.Config().load())
    else:
        print "Error. You typed the wrong confirmation."
        print "Exiting now.\n\n"
