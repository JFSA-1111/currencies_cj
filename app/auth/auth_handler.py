import time
from typing import Dict

import jwt

secret = 'please_update'
algorithm = 'HS256'


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, secret, algorithms=[algorithm])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 20
    }
    token = jwt.encode(payload, secret, algorithm=algorithm)

    return {"access_token": token}
