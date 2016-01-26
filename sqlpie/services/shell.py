# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

from flask import g
import thread, sys, os
import readline

import sqlpie

class Shell(object):

    ERROR_MESSAGE = "[Error] Invalid Command."
    LOADING_ERROR_MESSAGE = "[Error] Could Not Load File."

    def __init__(self, protocol, hostname, port):
        self.local_scope = {}
        sqlpie_hostname = "%s://%s:%s" % (protocol, hostname, port)
        # API responses will be in nicely formatted text
        self.sqlrc = sqlpie.sqlpie_client.SQLpieClient(sqlpie_hostname, json_responses=False)

    def handle_command(self, cmd):
        cmd = cmd.strip()
        is_assignment = cmd.split("=")
        response = []
        if len(is_assignment) == 2:
            k = is_assignment[0].strip()
            v = is_assignment[1].strip()
            if len(k)>0 and len(v)>0:
                if v in self.local_scope:
                    v = self.local_scope[v]
                self.local_scope[k]=v
            else:
                response.append(Shell.ERROR_MESSAGE)
        elif cmd in self.local_scope.keys():
            return self.local_scope[cmd]
        elif cmd.startswith("help"):
            if len(cmd) > 4:
                c = cmd[4:].strip()
                method = [method for method in dir(self.sqlrc) if callable(getattr(self.sqlrc, method)) and \
                     method.replace("_","") == c.replace("/","")]
                m = "".join(method)
                try:
                    response.append(getattr(self.sqlrc, m).__doc__.replace("\t\t",""))
                except:
                    response.append(Shell.ERROR_MESSAGE)
            else:
                response.append("\nShell-specific commands:\n===========================")
                commands = [method for method in dir(self.sqlrc) if callable(getattr(self.sqlrc, method)) and not method.startswith("_")]
                response.append("* help : show this list of available commands.")
                response.append("* exit : exit to the operating system, stopping all threads.")
                response.append("* load <bucket> <filename>: load TSV file contents into storage bucket.")
                response.append("* export <variable> <filename>: export results in variable to a local TXT file.")
                response.append("* <variable> = <json_object>: assign a value to a variable.")
                response.append("  _ is a special variable that contains the response from the latest executed API command.")
                response.append("\nAPI Endpoint commands:\n======================")
                for c in commands:
                    response.append("* %s" % (getattr(self.sqlrc, c ).__doc__.split("\n")[0],))
                response.append("")
                response.append("  To access more detailed documentation, type: help <API Endpoint>")
                response.append("  e.g.  help /document/put")
                response.append("")
        elif cmd == "exit":
            print "Exiting..."
            try:
                thread.interrupt_main()
            except KeyboardInterrupt:
                pass
            os._exit(1)
        elif cmd.startswith("load"):
            i = cmd.split(" ")
            if len(i) > 2:
                bucket = i[1]
                filename = " ".join(i[2:])
                try:
                    txt = open(filename)
                    data = txt.read()
                    headers = []
                    row_num = 0
                    for row in data.split("\n"):
                        row_num += 1
                        columns = row.split("\t")
                        if row_num == 1:
                            headers = columns
                        else:
                            if len(columns)==len(headers):
                                d = {}
                                for n, k in enumerate(headers):
                                    d[k] = columns[n]
                                d["_bucket"] = bucket
                                cmd = {"documents":d}
                                self.sqlrc._handler("/document/put", cmd)
                    response.append("[success] %s documents(s) loaded." % (row_num,))
                except:
                    response.append(Shell.LOADING_ERROR_MESSAGE)
            else:
                response.append(Shell.ERROR_MESSAGE)
        elif cmd.startswith("export"):
            i = cmd.split(" ")
            if len(i) > 2:
                variable = i[1]
                filename = " ".join(i[2:])
                try:
                    writer = open(filename, "w")
                    writer.write(self.local_scope[variable])
                    writer.close()
                    response.append("[success] Results exported to local file.")
                except:
                    response.append(Shell.LOADING_ERROR_MESSAGE)
            else:
                response.append(Shell.ERROR_MESSAGE)
        elif cmd.startswith("/"):
            i = cmd.split(" ")
            endpoint, cmd_params = i[0], {}
            if len(i) > 1:
                cmd_params = " ".join(i[1:])
            resp = self.sqlrc._handler(endpoint, cmd_params)
            self.local_scope["_"]=resp
            response.append("%s" % (resp,))
        elif cmd =="":
            response.append("")
        else:
            response.append(Shell.ERROR_MESSAGE)
        return "\n".join(response)