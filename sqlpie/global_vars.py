# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

import sqlpie

# The idea behind using this global_cache dictionary variable is just so it gets initialized here,
# and passed by reference once imported elsewhere.

global_cache = {}