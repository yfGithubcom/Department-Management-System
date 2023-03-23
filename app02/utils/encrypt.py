import hashlib
from django.conf import settings


def md5(data_str):
    salt = settings.SECRET_KEY
    obj = hashlib.md5(salt.encode('utf-8'))
    obj.update(data_str.encode('utf-8'))
    return obj.hexdigest()
