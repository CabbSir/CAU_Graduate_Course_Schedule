import time


def success(message = None):
    if message is None:
        message = {}
    data = {
        'code': 0,
        'message': message,
        'request_timestamp': int(time.time())
    }
    return data


def error(message = None):
    if message is None:
        message = {}
    data = {
        'code': message.get('code'),
        'message': message.get('message'),
        'request_timestamp': int(time.time())
    }
    return data