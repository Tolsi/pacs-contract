from serialize_image import serialize_image
import os

import sys

sys.path.append('../backend')

from node import register_face

CONTRACT_ID = "Adrq8E52S7GqcGP2jHg75fqxUCCmysBLaJMadXTqdFQm"
SENDER = "3Mrnkp5oc5NBuJgePjKZ5Yfn5heR3UKbCUN"

faces_dir = "../faces"

if __name__ == '__main__':
    [register_face(CONTRACT_ID, SENDER, file.split(".")[0], "Waves employee", serialize_image(os.path.join(faces_dir, file))) for file in os.listdir(faces_dir) if os.path.isfile(os.path.join(faces_dir, file))]