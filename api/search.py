# -*- coding: utf-8 -*-

import falcon
from sqlalchemy import text

from config import EVE_DB
from library.convert import json_encode
from api import generate_response


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
            rsp.body = json_encode(generate_response(1, 'query too short'))
            return
        rows = self.search(q)
        response = generate_response()
        response['data']['blueprint'] = [{'typeID': row[0], 'blueprintText': row[1]} for row in rows]
        rsp.body = json_encode(response)
