# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import sqlpie
import pyparsing
import re

class QueryParser:
    def operator_and(self, param):
        return self.expand_expression(param[0]) + " AND " + self.expand_expression(param[1])

    def operator_or(self, param):
        return self.expand_expression(param[0]) + " OR " + self.expand_expression(param[1])

    def operator_parenthesis(self, param):
        return "(" + self.expand_expression(param[0]) + ")"

    def operator_fields(self, param):
        field, value = param[0].split(":")[0], param[0].split(":")[1]
        flip = sqlpie.ContentKey.flip(field)
        if "%" in flip:
            flip_op = "LIKE"
        else:
            flip_op = "="
        content_keys = "SELECT key_id FROM content_keys WHERE content_key %s '%s'" % (flip_op, flip)

        sql = ""
        if field != sqlpie.Document.BUCKET_FIELD:
            quoted_values=re.findall(r'\"(.+)\"',value)
            date_values=re.findall(r'([\>\<\=]{0,2})([0-9]{2}\/[0-9]{2}\/[0-9]{4})|([\>\<\=]{0,2})([a-z]{3}\/[0-9]{2}\/[0-9]{4})',value)
            numeric_values=re.findall(r'([\>\<\=]{1,2})+([0-9\.\-]+)',value)
            if value == "=true" or value == "=false":
                boolean_values=[value[0],value[1:]]
            else:
                boolean_values=None
            if quoted_values:
                quoted_tokens = quoted_values[0].replace("_", " ").split()
                sql = self.operator_quotes([[c] for c in quoted_tokens], content_keys)
            elif date_values:
                sql_statements = []
                for i in date_values:
                    if i[1]:
                        op = i[0] #operator
                        value = sqlpie.Util.convert_to_date(i[1])
                    else:
                        op = i[2] #operator
                        value = sqlpie.Util.convert_to_date(i[3])
                    if op == "":
                        op = "="
                    sql_str =  "tf.document_id in (SELECT document_id FROM contents "
                    sql_str += "WHERE key_id IN (" + content_keys + ") AND numeric_value "
                    sql_str += "%s %s)" % (op, value)
                    sql_statements.append(sql_str)
                sql = " AND ".join(sql_statements)
            elif numeric_values:
                sql_statements = []
                for i in numeric_values:
                    op = i[0] #operator
                    value = i[1]
                    sql_str =  "tf.document_id in (SELECT document_id FROM contents "
                    sql_str += "WHERE key_id IN (" + content_keys + ") AND numeric_value "
                    sql_str += "%s %s)" % (op, value)
                    sql_statements.append(sql_str)
                sql = " AND ".join(sql_statements)
            elif boolean_values:
                op = boolean_values[0] #operator
                if boolean_values[1] == "true":
                    value = 1
                else:
                    value = 0
                sql =  "tf.document_id in (SELECT document_id FROM contents "
                sql += "WHERE key_id IN (" + content_keys + ") AND numeric_value "
                sql += "%s %s)" % (op, value)
            else:
                term_id = sqlpie.Term.get_key(param[0].split(":")[1])
                sql =  "tf.document_id in (SELECT document_id FROM content_terms "
                sql += "WHERE key_id IN (" + content_keys + ") AND term_id = UNHEX('%s'))" % (term_id,)

        return sql

    def operator_quotes(self, param, content_keys=False):
        search_terms = []
        term_ids = [sqlpie.Term.get_key(w[0]) for w in param]
        for idx, word in enumerate(term_ids):
            if idx == 0:
                sql =  "EXISTS (SELECT 1 FROM content_terms f%i WHERE f%i.term_id = UNHEX('%s') " % (idx, idx, word)
                sql += "AND f%i.document_id = tf.document_id AND f%i.bucket_id = tf.bucket_id " % (idx, idx)
                if content_keys:
                    sql += "AND f%i.key_id IN (" % (idx,)
                    sql += content_keys + ") "
                search_terms.append(sql)
            else:
                sql =  "AND EXISTS (SELECT 1 FROM content_terms f%i WHERE " % (idx,)
                sql += "f0.document_id = f%i.document_id AND f0.bucket_id = f%i.bucket_id " % (idx, idx)
                sql += "AND f0.key_id = f%i.key_id " % (idx,)
                sql += "AND f%i.term_id = UNHEX('%s') and f0.term_pos + %i = f%i.term_pos)" % (idx, word, idx, idx)
                search_terms.append(sql)
        if len(search_terms) > 0:
            search_terms.append(") ")
        return ' '.join(search_terms)

    def operator_term(self, param):
        word = param[0]
        sql = "tf.document_id in (SELECT document_id FROM ranking_tf where term_id = UNHEX('%s'))" 
        sql = sql % (sqlpie.Term.get_key(word),)
        return sql

    def operator_wildcard(self, param):
        word = param[0]
        sql =  "tf.document_id in (SELECT ct.document_id FROM content_terms ct WHERE ct.original LIKE \"%s\" " % (word+"%%",)
        sql += " AND tf.bucket_id = ct.bucket_id)"
        return sql

    def operator_not_term(self, param):
        return " NOT " + self.operator_term(param)

    def expand_expression(self, param):
        return getattr(self, "operator_" + param.getName())(param)

    def parse(self, query):
        parser = self.build_parser()
        return self.expand_expression(parser(query)[0])

    def build_parser(self):
        parsed_term = pyparsing.Group(pyparsing.Combine(pyparsing.Word(pyparsing.alphanums) + \
                                      pyparsing.Suppress('*'))).setResultsName('wildcard') | \
                      pyparsing.Group(pyparsing.Combine(pyparsing.Word(pyparsing.alphanums+"._") + \
                                      pyparsing.Word(':') + pyparsing.Group(pyparsing.Optional("\"") + \
                                      pyparsing.Optional("<") + pyparsing.Optional(">") + pyparsing.Optional("=") + \
                                      pyparsing.Optional("-") + pyparsing.Word(pyparsing.alphanums+"._/") + \
                                      pyparsing.Optional("&") + pyparsing.Optional("<") + pyparsing.Optional(">") + \
                                      pyparsing.Optional("=") + pyparsing.Optional("-") + \
                                      pyparsing.Optional(pyparsing.Word(pyparsing.alphanums+"._/")) + \
                                      pyparsing.Optional("\"")))).setResultsName('fields') | \
                      pyparsing.Group(pyparsing.Combine(pyparsing.Suppress('-')+ \
                                      pyparsing.Word(pyparsing.alphanums+"."))).setResultsName('not_term') | \
                      pyparsing.Group(pyparsing.Word(pyparsing.alphanums)).setResultsName('term')

        parsed_or = pyparsing.Forward()
        parsed_quote_block = pyparsing.Forward()
        parsed_quote_block << ((parsed_term + parsed_quote_block) | parsed_term )
        parsed_quote = pyparsing.Group(pyparsing.Suppress('"') + parsed_quote_block + \
                       pyparsing.Suppress('"')).setResultsName("quotes") | parsed_term
        parsed_parenthesis = pyparsing.Group((pyparsing.Suppress("(") + parsed_or + \
                             pyparsing.Suppress(")"))).setResultsName("parenthesis") | parsed_quote
        parsed_and = pyparsing.Forward()
        parsed_and << (pyparsing.Group(parsed_parenthesis + pyparsing.Suppress(pyparsing.Keyword("and")) + \
                       parsed_and).setResultsName("and") | \
                       pyparsing.Group(parsed_parenthesis + pyparsing.OneOrMore(~pyparsing.oneOf("or and") + \
                       parsed_and)).setResultsName("and") | parsed_parenthesis)
        parsed_or << (pyparsing.Group(parsed_and + pyparsing.Suppress(pyparsing.Keyword("or")) + \
                      parsed_or).setResultsName("or") | parsed_and)
        return parsed_or.parseString
