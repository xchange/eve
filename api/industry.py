# -*- coding: utf-8 -*-

import falcon
from sqlalchemy import text

from config import EVE_DB
from library.convert import json_encode
from api import generate_response


class BlueprintMaterialsHandler:
    sql = text('''
        SELECT aa.mapID,
               aa.mapText,
               aa.maxProductionLimit,
               aa.duration,
               aa.productTypeID,
               aa.productText,
               aa.productQuantity,
               aa.materialTypeID,
               aa.materialText,
               aa.quantity AS materialQuantity,
               bb.typeID   AS materialBlueprintTypeID,
               bb.activityID AS materialBlueprintActivityID
        FROM (
               SELECT x.mapID              AS mapID,
                      y.text               AS mapText,
                      x.maxProductionLimit AS maxProductionLimit,
                      x.duration           AS duration,
                      x.productTypeID      AS productTypeID,
                      z.text               AS productText,
                      x.productQuantity    AS productQuantity,
                      x.materialTypeID     AS materialTypeID,
                      w.text               AS materialText,
                      x.quantity
               FROM (
                      SELECT a.typeID             AS mapID,
                             a.maxProductionLimit AS maxProductionLimit,
                             b.time               AS duration,
                             c.productTypeID      AS productTypeID,
                             c.quantity           AS productQuantity,
                             d.materialTypeID     AS materialTypeID,
                             d.quantity           AS quantity
                      FROM industryblueprints AS a
                             LEFT JOIN industryactivity AS b ON b.activityID = 1 AND b.typeID = a.typeID
                             LEFT JOIN industryactivityproducts AS c ON c.activityID = 1 AND c.typeID = a.typeID
                             LEFT JOIN industryactivitymaterials AS d ON d.activityID = 1 AND d.typeID = a.typeID
                      WHERE a.typeID = :blueprint_id
                    ) AS x
                      LEFT JOIN trntranslations AS y ON y.tcID = 8
                 AND y.languageID = 'zh'
                 AND y.keyID = x.mapID
                      LEFT JOIN trntranslations AS z ON z.tcID = 8
                 AND z.languageID = 'zh'
                 AND z.keyID = x.productTypeID
                      LEFT JOIN trntranslations AS w ON w.tcID = 8
                 AND w.languageID = 'zh'
                 AND w.keyID = x.materialTypeID) AS aa
               LEFT JOIN industryactivityproducts AS bb ON bb.productTypeID = aa.materialTypeID
        ORDER BY aa.materialTypeID;
    ''')
    
    def query(self, blueprint_id: int):
        res = EVE_DB.execute(self.sql, blueprint_id=blueprint_id)
        return res.fetchall()

    def on_get(self, req: falcon.Request, rsp: falcon.Response):
        blueprint_id = req.get_param_as_int('id', required=True)
        rows = self.query(blueprint_id)
        if rows:
            result = {
                'blueprint': {
                    'typeID': rows[0][0],
                    'text': rows[0][1],
                    'maxProductionLimit': rows[0][2],
                    'duration': rows[0][3],
                },
                'product': {
                    'typeID': rows[0][4],
                    'text': rows[0][5],
                    'quantity': rows[0][6],
                },
                'materials': [],
            }
            for row in rows:
                result['materials'].append({
                    'typeID': row[7],
                    'text': row[8],
                    'quantity': row[9],
                    'blueprintID': -1 if row[10] is None else row[10],
                    'blueprintActivityID': -1 if row[11] is None else row[11],
                })
            response = generate_response()
            response['data'].update(result)
        else:
            response = generate_response(1, 'blueprint not found')
        rsp.body = json_encode(response)
