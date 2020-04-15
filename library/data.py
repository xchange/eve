# -*- coding: utf-8 -*-

import pandas
from sqlalchemy import text

import config


def search_industry():
    sql = '''
    SELECT a.typeID,
           a.activityID,
           b.text
    FROM industryactivity AS a
             LEFT JOIN trntranslations AS b ON b.keyID = a.typeID
    WHERE b.tcID = 8
      AND b.languageID = 'zh'
      AND a.activityID IN (1, 11)
    ORDER BY a.activityID, a.typeID
    '''
    df = pandas.read_sql(sql, config.EVE_DB)
    return df


EVE_INDUSTRY_SEARCH_DATA = search_industry()
