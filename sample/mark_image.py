import sys

from serialize_image import serialize_image
from node import mark_image

CONTRACT_ID = "H7XhErK1YzmY2i1EzNpfcSZv44vEFQGKLa89gUjsi15"
SENDER = "3N2ALKEtTHj2WBCxrmnCgBrf1AoTuv84bbF"

if __name__ == '__main__':
    mark_image(CONTRACT_ID, SENDER, serialize_image(sys.argv[1]))