from web3.auto import w3
import aiohttp
import asyncio
from helpers import hex_to_dec, clean_hex
import config
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

JSON_MEDIA_TYPE = 'application/json'
URL_LIST = config.NETWORKS[config.CONFIG["network"]]["uri_list"]


class RpcClient:

    def __init__(self):

        self.urls = [url for url in URL_LIST]
        self.current_id = 0

    async def _create_jsonrpc(self, method: str, params=None):

        params = params or []
        jsonrcp = {"id": self.current_id, "jsonrpc": "2.0", "method": method, "params": params}
        print(jsonrcp)
        self.current_id = +1
        return await self._multi_call(jsonrcp)

    @staticmethod
    async def call(json_payload, url):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.post(url, json=json_payload, headers={"Content-Type": JSON_MEDIA_TYPE})
                json_response = await response.json()
                print(json_response)
                if json_response.get("error"):
                    return json_response["error"]["code"], json_response["error"]["message"]
                else:
                    return json_response["result"]
            except aiohttp.ClientConnectorError as e:
                return {"success": False, "exception": e, "id": id}

    async def _multi_call(self, json_payload):
        tasks = []
        for url in self.urls:
            tasks.append(self.call(json_payload=json_payload, url=url))
        response = await asyncio.gather(*tasks)
        return response

    @staticmethod
    async def build_transaction(**kwargs):

        kwargs = kwargs["params"]
        params = {"chainId": config.NETWORKS[config.CONFIG["network"]]["chain_id"]}
        if "to" in kwargs:
            params["to"] = kwargs["to"]
        if "from" in kwargs:
            params["from"] = kwargs["from"]
        if "gas_amount" in kwargs:
            params["gas"] = hex(kwargs["gas_amount"])
        if "max_fee_per_gas" in kwargs:
            params["maxFeePerGas"] = kwargs["max_fee_per_gas"]
        if "max_priority_fee_per_gas" in kwargs:
            params["maxPriorityFeePerGas"] = clean_hex(kwargs["max_priority_fee_per_gas"])
        if "nonce" in kwargs:
            params["nonce"] = hex(kwargs["nonce"])
        if "value" in kwargs:
            params["value"] = clean_hex(kwargs["value"])
        if "data" in kwargs:
            params["data"] = kwargs["data"]
        return params

    async def call_contract(self, method_contract, contract_address, contract_param=None):

        if contract_param is not None:
            contract_param = [contract_param]
        else:
            contract_param = []

        data = await self.contract_instance.encodeABI(fn_name=method_contract, args=contract_param)
        parameters = await self.build_transaction(to=contract_address, data=data)

        return await self._create_jsonrpc(_method="eth_call", _params=[parameters, "latest"])

    async def call_contract_with_transaction(self, method_contract, contract_param=None, **kwargs):

        if contract_param is not None:
            contract_param = [contract_param]
        else:
            contract_param = []
        data = self.contract_instance.encodeABI(fn_name=method_contract, args=contract_param)

        params = kwargs
        print(params)
        params["params"]["data"] = data
        private_key = params["params"]["private_key"]
        params = params["params"]
        tx = await self.build_transaction(params=params)
        tx_signed = await self._sign_tx(transaction=tx, private_key=private_key)
        return await self._create_jsonrpc(method="eth_sendRawTransaction", params=[tx_signed.rawTransaction.hex()])

    @staticmethod
    async def _sign_tx(transaction, private_key):
        signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        return signed_tx


if __name__ == '__main__':
    pass


