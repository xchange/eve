# -*- coding: utf-8 -*-

import logging

import ujson

logger = logging.getLogger('Lib.Convert')


def json_encode(value):
    try:
        return ujson.dumps(value, ensure_ascii=False)
    except ValueError:
        logger.warning('JSON Encoding Failed: %s', value)
        return None
