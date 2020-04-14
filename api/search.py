# -*- coding: utf-8 -*-

import falcon
import ujson
from sqlalchemy import text

from config import EVE_DB


class BlueprintSearchHandler:
    sql = text('''
        SELECT
            a.typeID, b.text
        FROM
            industryblueprints AS a
        LEFT JOIN trntranslations AS b ON b.keyID = a.typeID
        WHERE
            b.tcID = 8
        AND b.languageID = 'zh'
        AND b.text LIKE :query
    ''')

    def search(self, q: str):
        res = EVE_DB.execute(self.sql, query='%{}%'.format(q))
        return res.fetchall()

    def on_get(self, req: falcon.Request, rsp: falcon.Response):
        q = req.get_param('q', required=True).strip()
        length = len(q)
        if length < 2 or length > 32:
            rsp.body = '[]'
            return
        rows = self.search(q)
        result = [{'typeID': row[0], 'blueprintText': row[1]} for row in rows]
        rsp.body = ujson.dumps(result, ensure_ascii=False)
