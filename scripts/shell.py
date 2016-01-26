# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import os, time
import sys
sys.path.append(os.getcwd())

from flask import Flask, current_app, g
from flask import jsonify
from flaskext.mysql import MySQL
import sqlpie

# load global vars
import application

def handle_shell(app, mysql, protocol, hostname, port):
    with application.app_context():
        print "Launching SQLpie Shell..."
        time.sleep(2)
        shell = sqlpie.Shell(protocol, hostname, port)

        pong = shell.handle_command("/ping")
        if pong.startswith("URLError"):
            print pong
            shell.handle_command("exit")
        else:
            print "type a command, or type help for a list of commands.\n"

        while(True):
            try:
                g.conn = mysql.connect()
                g.cursor = g.conn.cursor()
                g.conn.begin()

                cmd = raw_input("SQLpie # ")
                response = shell.handle_command(cmd)
                if len(response) > 1:
                    print response + "\n"

                g.conn.commit()
            except Exception as e:
                if sqlpie.Util.is_debug():
                    traceback.print_tb(sys.exc_info()[2])
                try:
                    g.conn.rollback()
                except:
                    pass
            finally:
                g.cursor.close()
                g.conn.close()

if __name__ == '__main__':
    protocol, hostname, port = "http", "localhost", sqlpie.Config.get(sqlpie.Config.SERVER_PORT)
    try:
        if "--protocol" in sys.argv[1:]:
            protocol = sys.argv[int(sys.argv[sys.argv.index("--protocol") + 1])]
        if "--hostname" in sys.argv[1:]:
            hostname = sys.argv[int(sys.argv.index("--hostname") + 1)]
        if "--port" in sys.argv[1:]:
            port = sys.argv[int(sys.argv.index("--port") + 1)]
        os.environ['sqlpie_debug'] = "False"
        application = Flask(__name__)
        sqlpie_config = sqlpie.Config().load()
        setup = sqlpie.DBSetup(sqlpie_config)
        setup.init(application)
        mysql = setup.db()
        with application.app_context():
            handle_shell(application, mysql, protocol, hostname, port)
    except:
        print "Error. Invalid Parameters."
        print "Exiting now.\n\n"
