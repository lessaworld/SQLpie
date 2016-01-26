# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import json
import sqlpie

class UtilTests(object):

    #
    # Util methods Tests
    #

    def test_util_walk(self):
        json_file = open('tests/_support_files/complex_object.json')
        json_str = json_file.read()
        d = json.loads(json_str)
        pairs = sqlpie.util.walk(d)
        assert pairs == [('float', u'errors.', u'nan'), ('float', u'errors.', u'inf'), ('unicode', u'name.', u'John Smith'), ('unicode', u'name.web.skills.', u'html'), ('unicode', u'years.web.skills.', u'5'), ('unicode', u'name.web.skills.', u'css'), ('unicode', u'years.web.skills.', u'3'), ('unicode', u'name.database.skills.', u'sql'), ('unicode', u'years.database.skills.', u'7'), ('bool', u'needs_visa.', u'False'), ('unicode', u'languages.', u'portuguese'), ('unicode', u'languages.', u'english'), ('unicode', u'languages.', u'spanish'), ('int', u'years_experience.', u'20'), ('float', u'score.', u'9.95'), ('unicode', u'city.location.', u'Pittsburgh'), ('unicode', u'state.location.', u'PA'), ('NoneType', u'certifications.', u'None'), ('bool', u'wear_glasses.', u'True')]