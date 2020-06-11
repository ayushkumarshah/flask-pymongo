import os


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "b'\xf0\xd3\x93\xa8<\xa5l\xfd\xde^\xd4\xc2v\xdc\xda\x07'"
    MONGODB_SETTINGS = { 'db': 'UTA_Enrollment',
                        'host': 'mongodb://localhost:27017/UTA_Enrollment'
                        }
    # host is optiona
