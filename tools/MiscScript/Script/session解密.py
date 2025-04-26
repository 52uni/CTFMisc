#!/usr/bin/env python3
import sys
import zlib
from base64 import b64decode
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode

def decryption(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)

    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True

    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode the payload because of '
                        'an exception')

    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress the payload before '
                            'decoding the payload')
                            
    return session_json_serializer.loads(payload)

if __name__ == '__main__':
	# 放置session
    print(decryption("eyJsb2dnZWRpbiI6dHJ1ZSwicm9sZSI6InVzZXIiLCJ1c2VybmFtZSI6IjEyMzQ1In0.ZCgLJA.HbW0QkSiIS4IK3Kk1IbE8o5rj-M".encode()))
