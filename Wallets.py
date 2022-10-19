from eth_account import Account
import secrets
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
import csv
import json
from web3.middleware import geth_poa_middleware
import config

PROVIDER ="https://api.avax-test.network/ext/bc/C/rpc"

def create_pair_publicPrivateKey(number):
    wallets = []
    for i in range(number):
        priv = secrets.token_hex(32)
        private_key = priv
        acct = Account.from_key(private_key)
        address_wallet = acct.address
        wallet = {"public_key": address_wallet,
                  "private_key": private_key,
                  "nonce": 0
        }
        wallets.append(wallet)
        with open("wallets_mint.json", 'w', encoding='utf-8') as f:
            json.dump(wallets, f, ensure_ascii=False, indent=4)
    return wallets

def transfert_avax(from_address,private_key,wallets,value):
    w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    file = open('wallets_mint.json', "r")
    wallets = json.loads(file.read())
    transfert_hash = []
    for elem in wallets:

        tx = {'chainId': 43113,
              'to': elem["public_key"],
              'gasPrice': get_gasPrice(),
              'gas': 21000,
              'nonce': get_nonce(from_address),
              'value': value,
              }

        tx_signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
        try:
            w3.eth.wait_for_transaction_receipt(tx_hash.hex())
            transfert_hash.append(tx_hash)
        except:
            print("error to broadcas the transaction")

    return transfert_hash

def get_gasPrice():
    w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    gas_price = w3.eth.gas_price
    return gas_price

def get_nonce(address):
    w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    nonce = w3.eth.get_transaction_count(address)
    return nonce

if __name__ == '__main__':
    pass