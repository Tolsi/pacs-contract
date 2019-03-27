from serialize_image import serialize_image
import os
import requests

NODE = "http://127.0.0.1:6862"
CONTRACT_ID = "H7XhErK1YzmY2i1EzNpfcSZv44vEFQGKLa89gUjsi15"
SENDER = "3N2ALKEtTHj2WBCxrmnCgBrf1AoTuv84bbF"

def register_face(name, details, image_base64):
    r = requests.post(NODE + '/contracts/execute', json={
        "contractId": CONTRACT_ID,
        "fee": 10000000,
        "sender": SENDER,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "ADD", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"},
            {"key": "name", "value": name, "type": "string"},
            {"key": "details", "value": details, "type": "string"}
         ]
    }, headers={'content-type': 'application/json', 'X-API-Key': 'vostok'})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

faces_dir = "../faces"

if __name__ == '__main__':
    [register_face(file.split(".")[0], "Waves employee", serialize_image(os.path.join(faces_dir, file))) for file in os.listdir(faces_dir) if os.path.isfile(os.path.join(faces_dir, file))]