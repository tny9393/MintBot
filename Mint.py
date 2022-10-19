from RpcClient import *


class MintBot(RpcClient):

    def __init__(self, from_address, private_key, contract_address, abi):
        RpcClient.__init__(self)
        self.contract_address = contract_address
        self.abi = abi
        self.from_address = from_address
        self.private_key = private_key
        self.contract_instance = w3.eth.contract(address=w3.toChecksumAddress(self.contract_address), abi=abi)

    async def allow_list_mint(self, quantity, **kwargs):
        method = "allowlistMint"
        print(self.contract_address)
        kwargs["params"]["from"] = self.from_address
        kwargs["params"]["private_key"] = self.private_key
        kwargs["params"]["to"] = self.contract_address
        params = kwargs["params"]
        await self.call_contract_with_transaction(method_contract=method, contract_param=quantity, params=params)

    async def public_mint(self, quantity, **kwargs):
        method = "publicMint"
        params = kwargs
        await self.call_contract_with_transaction(method_contract=method, contract_param=quantity, params=params)


if __name__ == '__main__':
    pass
