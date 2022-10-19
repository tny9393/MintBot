NETWORKS = {
    "avalanche_fujinet": {
        "chain_id": 43113,
        "uri_list": [
            "https://api.avax-test.network/ext/bc/C/rpc"
        ],
        "ws": "wss://api.avax-test.network/ext/bc/C/ws",
        "abi": "ressources/abi.json",
        "contract": "0x40643a28c3def3254Ba7B8485B59a7606ABb38bd",
        "snowtrace_api": "https://api-testnet.snowtrace.io/api",
    },
    "avalanche_mainnet": {
        "chain_id": 43114,
        "uri_list": [
            "https://api.avax.network/ext/bc/C/rpc"
        ],
        "ws": "wss://api.avax.network/ext/bc/C/ws",
        "abi": "ressources/abi.json",
        "contract": "0x0A50EE15688665C4bB98c802F5ee11fEc3DF0B80",
        "snowtrace_api": "https://api.snowtrace.io/api",
    }
}

CONFIG = {
    "network": "avalanche_fujinet",
    "wallets": "ressources/wallets_mint.json",
    "event": "Initialized",
    "gas_limit": 500_000,
    "maxFeePerGas": 300000000000,
    "maxPriorityFeePerGas": 50000000000,
    "value": 0,
    "quantity":1,
    "lag": 2,
}
