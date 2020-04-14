# -*- coding: utf-8 -*-

import os
import sys

from sqlalchemy import create_engine


EVE_DB_DSN = os.getenv('EVE_DB_DSN', '')
if not EVE_DB_DSN:
    print('未指定数据库地址, 程序终止')
    sys.exit(1)
EVE_DB = create_engine(EVE_DB_DSN, pool_recycle=3600, pool_size=2)
