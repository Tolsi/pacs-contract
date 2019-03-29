import sys

sys.path.append('../backend')

from serialize_image import serialize_image
from node import mark_image

CONTRACT_ID = "Adrq8E52S7GqcGP2jHg75fqxUCCmysBLaJMadXTqdFQm"
SENDER = "3Mrnkp5oc5NBuJgePjKZ5Yfn5heR3UKbCUN"

if __name__ == '__main__':
    mark_image(CONTRACT_ID, SENDER, serialize_image(sys.argv[1]))