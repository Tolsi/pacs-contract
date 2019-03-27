from .serialize_image import serialize_image
import os
import requests

def register_face(name, details, image_base64):
    r = requests.post('http://httpbin.org/post', json={
        "contractId": "2sqPS2VAKmK77FoNakw1VtDTCbDSa7nqh5wTXvJeYGo2",
        "fee": 10000000,
        "sender": "3PKyW5FSn4fmdrLcUnDMRHVyoDBxybRgP58",
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "ADD", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"},
            {"key": "name", "value": name, "type": "string"},
            {"key": "details", "value": details, "type": "string"}
         ]
    })
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

faces_dir = "root_dir"

if __name__ == '__main__':
    [register_face(file, "Waves employee", serialize_image(file)) for file in os.listdir(faces_dir) if os.path.isfile(os.path.join(faces_dir, file))]