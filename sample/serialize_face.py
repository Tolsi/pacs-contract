import face_recognition
import msgpack
import msgpack_numpy as m
import numpy as np
import base64
import sys

def serialize_face(image_path):
    data = face_recognition.load_image_file(image_path)
    faces = face_recognition.face_encodings(data)
    if len(faces) == 0:
        raise ValueError("Faces not detected")
    elif len(faces) > 1:
        raise ValueError('Too much faces detected')
    else:
        data = faces[0].astype(np.float16)
        data = msgpack.packb(data, default=m.encode)
        x_enc = base64.b64encode(data).decode("utf-8")
        return x_enc

if __name__ == '__main__':
    if sys.argv < 1:
        print("Pass a path to the image with a face")
        sys.exit(1)
    print(serialize_face(sys.argv[1]))