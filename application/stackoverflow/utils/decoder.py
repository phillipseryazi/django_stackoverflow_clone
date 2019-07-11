import jwt
import os


def decode_token(token):
    decoded = jwt.decode(token, os.environ['APP_SECRET'], algorithms=['HS256'])
    data = {'id': decoded['id'], 'isAdmin': decoded['isAdmin']}
    return data
