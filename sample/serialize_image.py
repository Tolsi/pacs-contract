import io
import base64
import sys

from PIL import Image

def serialize_image(image_path):
    im = Image.open(image_path)
    im.thumbnail([350, 350])
    bytes = io.BytesIO()
    im.save(bytes, format='JPEG', subsampling=2, quality=0)
    bytes.seek(0)
    data = bytes.read()
    x_enc = base64.b64encode(data)
    return x_enc

if __name__ == '__main__':

    if sys.argv < 1:
        print("Pass a path to the image")
        sys.exit(1)

    x_enc = serialize_image(sys.argv[1])
    print(len(x_enc))
    print(x_enc)