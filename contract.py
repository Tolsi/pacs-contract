import io
import json
import numpy as np
import os
import sys

import face_recognition
import msgpack
import msgpack_numpy as m
import base64
import requests
from PIL import Image

def params_objects_to_map(params):
    return dict((kv['key'], kv['value']) for kv in params)

def deserialize_narray(str):
    return msgpack.unpackb(base64.b64decode(str), object_hook=m.decode)

def serialize_narray(array):
    data = msgpack.packb(array.astype(np.float16), default=m.encode)
    return base64.b64encode(data).decode("utf-8")

def narray_from_image_bytes(bytes):
    image = Image.open(io.BytesIO(bytes))
    return np.array(image)[...,:3]

def check_valid_face_obj(obj):
    try:
        return obj['key'].startswith('face_')
    except:
        return False

# load registered faces from node API
def registered_face_encodings_with_ids():
    port = os.environ['NODE_PORT']
    contract_id = json.loads(os.environ['TX'])['contractId']
    if not port: sys.exit(1)
    url = 'http://node:{0}/contracts/{1}'.format(port, contract_id)
    r = requests.get(url, verify=False, timeout=2)
    data = r.json()
    faces_objs = list(filter(check_valid_face_obj, data))
    result = list(map(lambda x: {'name': x['key'][5:], 'encoding': deserialize_narray(x['value'][7:])}, faces_objs))
    return result


def recognize(image, known_face_encodings_with_names):
    face_encodings = encode_faces(image)

    known_face_names = list(map(lambda x: x['name'], known_face_encodings_with_names))
    known_face_encodings = list(map(lambda x: x['encoding'], known_face_encodings_with_names))

    found_face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        found_face_names.append(name)
    return found_face_names

def encode_faces(image_with_face):
    face_locations = face_recognition.face_locations(image_with_face)
    face_encodings = face_recognition.face_encodings(image_with_face, face_locations)
    return face_encodings

def json_to_string_without_spaces(obj):
    return json.dumps(obj, separators=(',', ':'))

if __name__ == '__main__':
    command = os.environ['COMMAND']
    if command == 'CALL':
        tx = json.loads(os.environ['TX'])
        params = params_objects_to_map(tx['params'])
        if 'cmd' not in params: sys.exit(3)
        cmd = params['cmd']
        if cmd == 'ADD':
            if 'photo' not in params or 'name' not in params or 'details' not in params: sys.exit(3)
            image = narray_from_image_bytes(base64.b64decode(params['photo'][7:].encode('utf-8')))
            found_faces = encode_faces(image)
            if len(found_faces) == 0: sys.exit(3)
            result = [{
                'key': 'face_' + tx['id'],
                'type': 'binary',
                'value': serialize_narray(found_faces[0])
            }]
            print(json_to_string_without_spaces(result))
        elif cmd == 'MARK':
            if 'photo' not in params:
                print("there is not photo: params")
                sys.exit(3)
            image = narray_from_image_bytes(base64.b64decode(params['photo'][7:].encode('utf-8')))
            registered_faces = registered_face_encodings_with_ids()
            found_face_ids = recognize(image, registered_faces)
            ts = 'mark_' + str(tx['timestamp'])
            result = [{
                'key': ts,
                'type': 'string',
                'value': json_to_string_without_spaces(found_face_ids)
            }]
            print(json_to_string_without_spaces(result))
        else:
            sys.exit(3)
    elif command == 'CREATE':
        sys.exit(0)
    else:
        sys.exit(3)
