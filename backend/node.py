import itertools
import json

import requests
from itertools import islice

NODE = 'http://127.0.0.1:6862'

def mark_image(contract_id, sender, image_base64):
    r = requests.post(NODE + '/transactions/sign', json={
	    "broadcast": True,
		"type": 104,
        "contractId": contract_id,
        "fee": 15000000,
        "sender": sender,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "MARK", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"}
        ]
    }, headers={'content-type': 'application/json', 'X-API-Key': 'vostok'})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

def register_face(contract_id, sender, name, details, image_base64):
    r = requests.post(NODE + '/transactions/sign', json={
        "broadcast": True,
		"type": 104,
		"contractId": contract_id,
        "fee": 15000000,
        "sender": sender,
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

def get_current_height():
    return requests.get(NODE + '/blocks/height').json()['height']

def get_blocks_in_range(fr, to_exclusive):
    def window(seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def blocks_range_request(fr, to):
        return requests.get(NODE + '/blocks/seq/' + str(fr) + '/' + str(to)).json()

    if fr == to_exclusive:
        return blocks_range_request(fr, to_exclusive)

    result = []
    range_from_to_by_99_and_last = range(fr, to_exclusive, 99)
    if (fr - to_exclusive) % 99 != 0:
        range_from_to_by_99_and_last = itertools.chain(range(fr, to_exclusive + 1, 99), [to_exclusive + 1])
    for (f, t) in window(range_from_to_by_99_and_last, 2):
        result += blocks_range_request(f, t - 1)
    return result

if __name__ == '__main__':
    # print(current_height())
    # print(list(grouper(2, [2,4,6], 7)))
    blocks = get_blocks_in_range(1, get_current_height())
    print([block['transactions'] for block in blocks])