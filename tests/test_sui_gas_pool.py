import os
import pytest
import httpx
import json
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
    gas_reservation = await sgp.reserve_gas(
        gas_budget=1_000_000_000,
        reserve_duration_secs=60,
    )
    assert gas_reservation is not None


@pytest.mark.asyncio
async def test_execute_tx():
    gas_reservation = await sgp.reserve_gas(
        gas_budget=500_000_000,
        reserve_duration_secs=30,
    )
    assert gas_reservation is not None
    print(gas_reservation)
    tx_result = await sgp.execute_tx(
        tx_bytes="AAABACBZeZbWRXCxun7AI3aZX+Em1EMNOFpilw8zJm1+txEXLwIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIEY29pbgR6ZXJvAQcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgNzdWkDU1VJAAABAQIAAAEAAFl5ltZFcLG6fsAjdplf4SbUQw04WmKXDzMmbX63ERcvCbb/HivXAvtzjv6yDzC5BpDSHS8Y1D11T80EdLhU/DutJ+Y7FQAAAAAgsOlox+HIoXhcSjSpwqyHLNsN7+WGlJ0vksa5+pPnUK8EYFsCu2mKdoinPEhCRwoLnZptPN4afZoSNRHaFd3LFArlOxUAAAAAIFFuHmaembiOVT8BsJUBCUGDCdah8f77N8lSkZW1m/PATo4PloJ1kGQRIgBKQ15Qey61HqiSf5uRJBGKoSC1QcEJ5TsVAAAAACDeUgKuFYV/B/rh1TQJLYM8OKbqeCzPQc4p0JzHKtQjqADQsrg2g+nw+uh+rI774czQZdIgQYpf5mJaeWPJ1Q0p9OQ7FQAAAAAgll4uBXh+nAargEdZMD1E8a1LrYHajHriFB3kVC6AsukBfolW3HnmfMZragllTXbsjzqVHTJKKKBRl/O9F9PSVPTkOxUAAAAAIAhbS5DSaZ+nvDK9s+17MPwR4Bt6v0o+mcYibFm6G839AbmbxZgVqU5l9r8pbwHyqu1qcF10p8AwG5rSLNbkITj05DsVAAAAACAHtw26b7Si0Z74jCQlZfk005yrfH6v9R7KlE0+vEeWrgIXKKcrwtvF9t4Lj5lQh69xq2fSqjflL4Ndl6piDSba9OQ7FQAAAAAgOIJeam3lkI0sSS0WRjFRuE/nNvWgN8u1X2LbmEKY/RQCN0G5RmHbgXSGpyVBtixnFqprE3BzHuuPmJGT/7f5gfTkOxUAAAAAIDmhkmShdfxnagyqMrpWgw93/su39lfFqae5xXMwBP7UAxgozbtFvq1vW5Ah2wgnTFc/VJrvChV9UIhUqsTFoAr05DsVAAAAACCP/ScikDfibzCfMfU8NN/Xvtn9DA1BSGyG9mvHmMKW619picFnEAPIg7u9g4JBKq5AvDcfZz6Vzob/enFskur26AMAAAAAAAAAypo7AAAAAAA=",
        reservation_id=gas_reservation.reservation_id,
        user_sig="ACeMOYQAxWDTtwQAoyugHsen4yBUkmAH83YwHcdGobVO3I//C+if+JxPWEsLjuafCoLYMC5RmnLJyK4rkRp6iggZrWQv6j41gxJgqNjz1GEJWdRxU6gK7pLWuRR2LA/jTA==",
    )
    print(tx_result)
    print(json.dumps(tx_result, indent=4))
