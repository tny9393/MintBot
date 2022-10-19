import requests
import json
from web3 import Web3
from web3.exceptions import MismatchedABI
from web3._utils.events import normalize_event_input_types, get_event_abi_types_for_decoding, get_abi_input_names, exclude_indexed_event_inputs
from web3.types import ABIEvent
from eth_abi import decode_abi
from eth_utils.curried import hexstr_if_str, to_bytes


def hex_to_dec(x):
    '''
    Convert hex to decimal
    '''
    return int(x, 16)


def clean_hex(d):
    '''
    Convert decimal to hex and remove the "L" suffix that is appended to large
    numbers
    '''
    return hex(d).rstrip('L')


def wei_to_ether(wei):
    '''
    Convert wei to ether
    '''
    return 1.0 * wei / 10 ** 18


def ether_to_wei(ether):
    '''
    Convert ether to wei
    '''
    return ether * 10 ** 18


def get_abi(address, url):
    params = {"module": "contract", "action": "getabi", "address": address}
    response = requests.get(url, params=params)
    abi = json.loads(response.content.decode())
    with open("ressources/abi.json", 'w') as file:
        file.write(abi["result"])
    return abi["result"]


def load_json_file(json_file):
    return json.load(open(json_file, "r"))


def make_signature(event):
    """
    Parses the ABI into an event signature
    Args:
        event (dict): the event ABI
    Returns:
        (str): the signature
    """
    types = ','.join([t['type'] for t in event['inputs']])
    return '{name}({types})'.format(name=event['name'], types=types)


def find_event(event_name, abi):
    """
    Look for the event in the abi
    Args:
        event_name (str): the event name
        abi (list): the contract abi
    Returns:
        (dict): the event
    """
    for elem in abi:
        if 'name' in elem and elem["type"] == 'event' and elem['name'] == event_name:
            return elem


def make_topic0(event) -> str:
    """
    Calculates the event topic hash from the event ABI
    Args:
        event (dict): the event ABI
    Returns:
        (str): the event topic as 0x prepended hex
    """
    topic_hex = Web3.keccak(text=make_signature(event)).hex()
    return topic_hex


def get_event_data(event_abi, log):
    if event_abi['anonymous']:
        log_topics = log['topics']
    elif not log['topics']:
        raise MismatchedABI("Expected non-anonymous event to have 1 or more topics")
    elif make_topic0(event_abi) != log['topics'][0]:
        raise MismatchedABI("The event signature did not match the provided ABI")
    else:
        log_topics = log['topics'][1:]

    log_data = hexstr_if_str(to_bytes, log['data'])

    log_data_abi = exclude_indexed_event_inputs(event_abi)
    log_data_normalized_inputs = normalize_event_input_types(log_data_abi)
    log_data_types = get_event_abi_types_for_decoding(log_data_normalized_inputs)
    log_data_names = tuple(get_abi_input_names(ABIEvent({'inputs': log_data_abi})))

    decoded_log_data = decode_abi(log_data_types, log_data)
    event_data = dict(zip(log_data_names, decoded_log_data))

    return event_data


if __name__ == '__main__':
    get_abi(address="0x0A50EE15688665C4bB98c802F5ee11fEc3DF0B80", url="https://api.snowtrace.io/api")
