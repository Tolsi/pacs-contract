import sys

from .serialize_image import serialize_image
import requests

def mark_image(image_base64):
    r = requests.post('http://httpbin.org/post', json={
        "contractId": "2sqPS2VAKmK77FoNakw1VtDTCbDSa7nqh5wTXvJeYGo2",
        "fee": 10000000,
        "sender": "3PKyW5FSn4fmdrLcUnDMRHVyoDBxybRgP58",
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "MARK", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"}
        ]
    })
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

if __name__ == '__main__':
    mark_image(serialize_image(sys.argv[1]))