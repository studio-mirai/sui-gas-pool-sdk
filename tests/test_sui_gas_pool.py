import os
import pytest
import httpx
from sui_gas_pool_sdk.sui_gas_pool import SuiGasPool
from dotenv import load_dotenv

load_dotenv()

SUI_GAS_POOL_URL = os.environ["SUI_GAS_POOL_URL"]
SUI_GAS_POOL_AUTH_TOKEN = os.environ["SUI_GAS_POOL_AUTH_TOKEN"]
SUI_RPC_URL = os.environ["SUI_RPC_URL"]

http_client = httpx.AsyncClient()

sgp = SuiGasPool(
    gas_pool_url=SUI_GAS_POOL_URL,
    gas_pool_auth_token=SUI_GAS_POOL_AUTH_TOKEN,
    sui_rpc_url=SUI_RPC_URL,
    http_client=http_client,
)


@pytest.mark.asyncio
async def test_reserve_gas():
    reservation = await sgp.reserve_gas(
        gas_budget=1_000_000_000,
        reserve_duration_secs=60,
    )
    print(reservation)
    assert reservation is not None
