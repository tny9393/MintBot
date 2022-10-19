import multiprocessing
from Mint import *
import config
from helpers import *


def thr(from_address, private_key, nonce):
    # we need to create a new loop for the thread, and set it as the 'default'
    # loop that will be returned by calls to asyncio.get_event_loop() from this
    # thread.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(mint(from_address=from_address, private_key=private_key, nonce=nonce))
    loop.close()


async def mint(from_address, private_key, nonce):
    Mint = MintBot(from_address=from_address, private_key=private_key,
                   contract_address=config.NETWORKS[config.CONFIG["network"]]["contract"],
                   abi=load_json_file(config.NETWORKS[config.CONFIG["network"]]["abi"]))
    params = {"gas_amount": config.CONFIG["gas_limit"],
              "max_fee_per_gas": config.CONFIG["maxFeePerGas"],
              "max_priority_fee_per_gas": config.CONFIG["maxPriorityFeePerGas"],
              "value": config.CONFIG["value"],
              "nonce": nonce}
    print(params)
    await Mint.allow_list_mint(quantity=config.CONFIG["quantity"], params=params)


def start_mint():
    wallets = load_json_file(config.CONFIG["wallets"])
    processes = [multiprocessing.Process(target=thr, kwargs=params) for params in wallets]
    [t.start() for t in processes]
    [t.join() for t in processes]


if __name__ == '__main__':
    start_mint()
