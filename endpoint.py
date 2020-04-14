# -*- coding: utf-8 -*-

import logging
from wsgiref.simple_server import make_server

import falcon

from api.search import BlueprintSearchHandler

logger = logging.getLogger('EndPoint')

api = falcon.API()
api.add_route('/search/blueprint', BlueprintSearchHandler())


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 10001, api)
    logger.info("API服务器已启动，监听 %s:%d", '127.0.0.1', 10001)
    httpd.serve_forever()
