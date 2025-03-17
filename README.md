sui-gas-pool-sdk

This is a Python SDK for interacting with an instance of [sui-gas-pool](https://github.com/MystenLabs/sui-gas-pool).

## How to Use

To make a sponsored transaction, create an instance of `SuiGasPool` with:

* `gas_pool_url`: URL endpoint for your `sui-gas-pool` service.
* `gas_pool_auth_token`: Authorzation token for your `sui-gas-pool` service.
* `sui_rpc_url`: A Sui RPC endpoint URL, should be the same network as your `sui-gas-pool` service.
* `http_client` (Optional) – an instance of `httpx.AsyncClient`.

```
http_client = httpx.AsyncClient()

sgp = SuiGasPool(
    gas_pool_url=SUI_GAS_POOL_URL,
    gas_pool_auth_token=SUI_GAS_POOL_AUTH_TOKEN,
    sui_rpc_url=SUI_RPC_URL,
    http_client=http_client,
)

tx_digest = sgp.sponsor_and_execute_tx(
    tx_bytes: "AAABACBZeZbWRXCxun7AI3aZX+Em1EMNOFpilw8zJm1...",
    gas_budget: 1_000_000_000,
    reserve_duration_secs: 10,
)
```