# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flaskext.mysql import MySQL
import sqlpie
import os, json, traceback, sys

class DBSetup(object):
    def __init__(self, config={}):
        self.config = config

    def init(self, app):
        self.mysql = MySQL()
        params = self.get_database_params()
        app.config['MYSQL_DATABASE_USER'] = params['MYSQL_DATABASE_USER']
        app.config['MYSQL_DATABASE_PASSWORD'] = params['MYSQL_DATABASE_PASSWORD']
        app.config['MYSQL_DATABASE_DB'] = params['MYSQL_DATABASE_DB']
        app.config['MYSQL_DATABASE_HOST'] = params['MYSQL_DATABASE_HOST']
        app.config['MYSQL_DATABASE_PORT'] = params['MYSQL_DATABASE_PORT']

        self.mysql.init_app(app)

    def db(self):
        return self.mysql

    def get_database_params(self):
        ret = {}
        if os.environ.get('mysql_database_user') and os.environ.get('mysql_database_password') and \
            os.environ.get('mysql_database_db') and os.environ.get('mysql_database_host') and \
            os.environ.get('mysql_database_port'):
            ret['MYSQL_DATABASE_USER'] = os.environ.get('mysql_database_user')
            ret['MYSQL_DATABASE_PASSWORD'] = os.environ.get('mysql_database_password')
            ret['MYSQL_DATABASE_DB'] = os.environ.get('mysql_database_db')
            ret['MYSQL_DATABASE_HOST'] = os.environ.get('mysql_database_host')
            ret['MYSQL_DATABASE_PORT'] = int(os.environ.get('mysql_database_port'))
        else:
            env = sqlpie.DBSetup.environment()

            if env in self.config['db']:
                ret['MYSQL_DATABASE_USER'] = self.config['db'][env]['mysql_database_user']
                ret['MYSQL_DATABASE_PASSWORD'] = self.config['db'][env]['mysql_database_password']
                ret['MYSQL_DATABASE_DB'] = self.config['db'][env]['mysql_database_db']
                ret['MYSQL_DATABASE_HOST'] = self.config['db'][env]['mysql_database_host']
                ret['MYSQL_DATABASE_PORT'] = int(self.config['db'][env]['mysql_database_port'])
            else:
                ret['MYSQL_DATABASE_USER'] = None
                ret['MYSQL_DATABASE_PASSWORD'] = None
                ret['MYSQL_DATABASE_DB'] = None
                ret['MYSQL_DATABASE_HOST'] = None
                ret['MYSQL_DATABASE_PORT'] = None
        return ret

    @staticmethod
    def environment():
        env = "development"
        if os.environ.get('sqlpie_env'):
            env = os.environ.get('sqlpie_env').lower()
        return env

    @staticmethod
    def reset_database():
        sqlpie.Bucket.reset()
        sqlpie.Document.reset()
        sqlpie.Content.reset()
        sqlpie.Term.reset()
        sqlpie.ContentKey.reset()
        sqlpie.ContentTerm.reset()
        sqlpie.RankingIDF.reset()
        sqlpie.RankingTF.reset()
        sqlpie.Observation.reset()
        sqlpie.Predicate.reset()
        sqlpie.Cache.reset()
        sqlpie.Model.reset()
        sqlpie.ModelClassifier.reset()

    @staticmethod
    def create_database(app, sqlpie_config):
        config_mysql = MySQL()
        env = sqlpie.DBSetup.environment()
        curr_db_config = sqlpie_config['db'][env]['mysql_database_db']
        app.config['MYSQL_DATABASE_DB'] = "mysql"
        app.config['MYSQL_DATABASE_PASSWORD'] = sqlpie_config['db'][env]['mysql_database_password']
        app.config['MYSQL_DATABASE_USER'] = sqlpie_config['db'][env]['mysql_database_user']
        app.config['MYSQL_DATABASE_HOST'] = sqlpie_config['db'][env]['mysql_database_host']
        app.config['MYSQL_DATABASE_PORT'] = sqlpie_config['db'][env]['mysql_database_port']
        config_mysql.init_app(app)

        try:
            local_conn = config_mysql.connect()
            local_cursor = local_conn.cursor()
            drop_db_sql_command = "DROP DATABASE IF EXISTS SQLpie_%s; " % (env);
            local_cursor.execute(drop_db_sql_command)
            local_cursor.close()

            local_cursor = local_conn.cursor()
            create_db_sql_command = "CREATE DATABASE SQLpie_%s; " % (env);
            use_db_sql_command = "USE SQLpie_%s; " % (env);
            f = open("sqlpie/db/sql/schema.sql","r")
            schema = f.read()
            sql_commands = create_db_sql_command + use_db_sql_command + schema
            local_cursor.execute(sql_commands)
            local_cursor.close()

            local_cursor = local_conn.cursor()
            f = open("sqlpie/db/sql/seed.sql","r")
            seed_commands = f.read()
            sql_commands = use_db_sql_command + seed_commands
            local_cursor.execute(seed_commands)
            local_conn.commit()
            print "Successfully created SQLpie_%s database on %s server." % (env, sqlpie_config['db'][env]['mysql_database_host'])
        except Exception as e:
            print "[Error] creating SQLpie_%s database on %s server." % (env, sqlpie_config['db'][env]['mysql_database_host'])
            if sqlpie.Util.is_debug():
                traceback.print_tb(sys.exc_info()[2])
        finally:
            try:
                local_cursor.close()
                local_conn.close()
            except:
                pass

        app.config['MYSQL_DATABASE_DB']    = curr_db_config
