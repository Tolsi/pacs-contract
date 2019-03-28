import json
from datetime import datetime
from time import sleep

import dataset
from sqlalchemy import JSON

from node import get_blocks_in_range, get_current_height

WAIT_CONFIRMATIONS = 1
CONTRACT_ID = "H7XhErK1YzmY2i1EzNpfcSZv44vEFQGKLa89gUjsi15"

# init db
db = dataset.connect('sqlite:///db.sqlite')
db.query('PRAGMA journal_mode=wal')

employees_table = db.create_table('employees',
                                  primary_id='id',
                                  primary_type=db.types.text)
marks_table = db.create_table('marks',
                              primary_id='id',
                              primary_type=db.types.datetime)
marks_table.create_column(name='employees', type = JSON)
settings_table = db.create_table('settings',
                                 primary_id='id',
                                 primary_type=db.types.text)


def load_current_block():
    current_block = settings_table.find_one(id='current_block')
    if current_block is None:
        settings_table.upsert(dict(id='current_block', value=1), ['id'])
        current_block = 1
    else:
        current_block = current_block['value']
    return current_block


def save_current_block(new_current_block):
    settings_table.upsert(dict(id='current_block', value=new_current_block), ['id'])


def params_objects_to_map(params):
    return dict((kv['key'], kv['value']) for kv in params)


current_block = load_current_block()
while True:
    next_height = get_current_height() - WAIT_CONFIRMATIONS
    if next_height > current_block:
        print('process from ' + str(current_block) + ' to ' + str(next_height))
        blocks = get_blocks_in_range(current_block, next_height)
        db.begin()
        for block in blocks:
            print(block)
            print('processing ' + block['signature'])
            if len(block['transactions']) > 0:
                executed_call_contract_txs = filter(
                    lambda tx: 'tx' in tx and tx['tx']['type'] == 104 and tx['tx']['contractId'] == CONTRACT_ID,
                    block['transactions'])


                def params_results_and_tx_id(executed_tx):
                    p = params_objects_to_map(executed_tx['tx']['params'])
                    r = params_objects_to_map(executed_tx['results'])
                    result = {**p, **r}
                    result['tx_id'] = executed_tx['tx']['id']
                    return result


                call_params_and_results_contract_objects = map(params_results_and_tx_id, executed_call_contract_txs)
                for call_contract_object in call_params_and_results_contract_objects:
                    cmd = call_contract_object['cmd']
                    if cmd == 'ADD':
                        employees_table.insert(dict(id=call_contract_object['tx_id'],
                                                    name=call_contract_object['name'],
                                                    details=call_contract_object['details'],
                                                    photo=call_contract_object['photo']))
                    elif cmd == 'MARK':
                        at_key = next(filter(lambda x: x.startswith('mark_'),call_contract_object.keys()), None)
                        at = int(at_key[5:]) / 1000
                        marks_table.insert(dict(id=datetime.fromtimestamp(at),
                                                employees=json.loads(call_contract_object[at_key]),
                                                mark_photo=call_contract_object['photo']))
        save_current_block(next_height)
        db.commit()
        current_block = next_height
    else:
        print('there\'re no new blocks')
    sleep(30)
