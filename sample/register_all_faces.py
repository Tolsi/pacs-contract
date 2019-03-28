from serialize_image import serialize_image
import os
from node import register_face

CONTRACT_ID = "H7XhErK1YzmY2i1EzNpfcSZv44vEFQGKLa89gUjsi15"
SENDER = "3N2ALKEtTHj2WBCxrmnCgBrf1AoTuv84bbF"

faces_dir = "../faces"

if __name__ == '__main__':
    [register_face(CONTRACT_ID, SENDER, file.split(".")[0], "Waves employee", serialize_image(os.path.join(faces_dir, file))) for file in os.listdir(faces_dir) if os.path.isfile(os.path.join(faces_dir, file))]