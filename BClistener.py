import asyncio
import websockets
from helpers import *
from datetime import datetime
import datetime as dt
import config
from MultiMinter import *

URL = config.NETWORKS[config.CONFIG["network"]]["ws"]


async def get_events(id, params, queue):
    async with websockets.connect(URL) as ws:

        await ws.send(json.dumps({"id": 1, "method": "eth_subscribe", "params": params}))
        subscription_response = await ws.recv()
        subscription_response = json.loads(subscription_response)

        if subscription_response.get("error"):
            return subscription_response["error"]["code"], subscription_response["error"]["message"]
        else:
            print(f"Subscribed with success to stream id: {subscription_response['result']}")

        while True:
            message = await ws.recv()
            await queue.put((id, message))


async def on_message(queue):
    block_timestamp, start_mint_time = None, None
    while True:
        id, value = await queue.get()

        if id == "block_timestamp":
            block_timestamp = hex_to_dec(json.loads(value)['params']['result']["timestamp"])
            block_time = datetime.fromtimestamp(block_timestamp)
        else:
            start_mint_data = (json.loads(value)['params']['result'])
            event_abi = find_event(event_name=config.CONFIG["event"],
                                   abi=load_json_file(config.NETWORKS[config.CONFIG["network"]]["abi"]))
            start_mint_time = datetime.fromtimestamp(get_event_data(event_abi, start_mint_data)["allowlistStartTime"])

        if start_mint_time is not None:
            if (start_mint_time - dt.timedelta(seconds=config.CONFIG["lag"])) <= block_time:
                return start_mint()


async def event_listener():
    params1 = ["newHeads"]

    event = find_event(config.CONFIG["event"], load_json_file(config.NETWORKS[config.CONFIG["network"]]["abi"]))
    topic = make_topic0(event)
    print(topic)
    params2 = ["logs", {"address": [config.NETWORKS[config.CONFIG["network"]]["contract"]], "topics": [topic]}]
    print(config.NETWORKS[config.CONFIG["network"]]["contract"])
    queue = asyncio.Queue()

    task1 = asyncio.create_task(get_events("block_timestamp", params1, queue))
    task2 = asyncio.create_task(get_events("mint_start", params2, queue))
    task3 = asyncio.create_task(on_message(queue))
    await asyncio.wait([task1, task2, task3], return_when=asyncio.FIRST_COMPLETED)


def run_event_listener():
    asyncio.run(event_listener())


if __name__ == '__main__':
    run_event_listener()
