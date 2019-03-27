import sys

from serialize_image import serialize_image
import requests

NODE = "http://127.0.0.1:6862"
CONTRACT_ID = "H7XhErK1YzmY2i1EzNpfcSZv44vEFQGKLa89gUjsi15"
SENDER = "3N2ALKEtTHj2WBCxrmnCgBrf1AoTuv84bbF"

def mark_image(image_base64):
    r = requests.post(NODE + '/contracts/execute', json={
        "contractId": CONTRACT_ID,
        "fee": 10000000,
        "sender": SENDER,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "MARK", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"}
        ]
    }, headers={'content-type': 'application/json', 'X-API-Key': 'vostok'})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

if __name__ == '__main__':
    mark_image(serialize_image(sys.argv[1]))