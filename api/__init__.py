# -*- coding: utf-8 -*-

import copy

response_ok = {
    'errorCode': 0,
    'data': {},
}

response_fail = {
    'errorCode': 1,
    'data': {
        'errorMessage': '',
    }
}


def generate_response(error_code: int = 0, error_message: str = ''):
    if error_code == 0:
        return copy.deepcopy(response_ok)
    else:
        response = copy.deepcopy(response_fail)
        response['errorCode'] = error_code
        response['data']['errorMessage'] = error_message
        return response
