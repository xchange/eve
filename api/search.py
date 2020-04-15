# -*- coding: utf-8 -*-

import falcon

from config import EVE_DB
from library.convert import json_encode
from library.data import EVE_INDUSTRY_SEARCH_DATA as INDUSTRY
from api import generate_response


def search(q: str, activity_id: int):
    df = INDUSTRY[(INDUSTRY['activityID'] == activity_id) & (INDUSTRY['text'].str.contains(q))]
    if df.empty:
        return []
    else:
        return [item for item in df.values]


class BlueprintSearchHandler:
    def on_get(self, req: falcon.Request, rsp: falcon.Response):
        q = req.get_param('q', required=True).strip()
        length = len(q)
        if length < 2 or length > 32:
            rsp.body = json_encode(generate_response(1, 'query too short'))
            return
        rows = search(q, 1)
        response = generate_response()
        response['data']['blueprint'] = [{'typeID': row[0], 'blueprintText': row[2]} for row in rows]
        rsp.body = json_encode(response)


class ReactionSearchHandler:
    def on_get(self, req: falcon.Request, rsp: falcon.Response):
        q = req.get_param('q', required=True).strip()
        length = len(q)
        if length < 2 or length > 32:
            rsp.body = json_encode(generate_response(1, 'query too short'))
            return
        rows = search(q, 11)
        response = generate_response()
        response['data']['reaction'] = [{'typeID': row[0], 'reactionText': row[2]} for row in rows]
        rsp.body = json_encode(response)
