import httpx
from types import TracebackType
from typing import Optional, Type
from dataclasses import dataclass
from sui_gas_pool_sdk.exceptions import GasReservationDurationTooLongException


@dataclass
class GasReservation:
    reservation_id: int
    gas_budget: int
    reserve_duration_secs: int
    created_at: int
    expires_at: int


class SuiGasPool:
    """
    A class for interacting with Sui Gas Pool.
    """

    def __init__(
        self,
        gas_pool_url: str,
        gas_pool_auth_token: str,
        sui_rpc_url: str,
        http_client: httpx.AsyncClient | None = None,
    ):
        """
        Initialize the SuiGasPool client.

        Args:
            base_url: The base URL for the Sui Gas Pool API.
            client: An optional httpx.AsyncClient instance. If not provided, a new one will be created.
        """

        self.gas_pool_url = gas_pool_url
        self.gas_pool_auth_token = gas_pool_auth_token
        self.sui_rpc_url = sui_rpc_url

        self.http_client = http_client or httpx.AsyncClient()
        self._owns_client = http_client is None

    async def execute_tx(
        self,
        tx_bytes: str,
        reservation_id: int,
        user_sig: str,
    ):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gas_pool_auth_token}",
        }
        data = {
            "reservation_id": reservation_id,
            "tx_bytes": tx_bytes,
            "user_sig": user_sig,
        }

        r = await self.http_client.post(
            url=f"{self.gas_pool_url}/v1/execute_tx",
            headers=headers,
            json=data,
        )
        return r.json()

    async def reserve_gas(
        self,
        gas_budget: int,
        reserve_duration_secs: int,
    ) -> GasReservation:
        if reserve_duration_secs > 600:
            raise GasReservationDurationTooLongException()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gas_pool_auth_token}",
        }
        data = {
            "gas_budget": gas_budget,
            "reserve_duration_secs": reserve_duration_secs,
        }
        r = await self.http_client.post(
            url=f"{self.gas_pool_url}/v1/reserve_gas",
            headers=headers,
            json=data,
        )
        return r.json()

    async def _sui_get_events(
        self,
        tx_digest: str,
    ):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sui_getEvents",
            "params": [tx_digest],
        }
        headers = {
            "Content-Type": "application/json",
        }
        r = await self.http_client.post(
            url=self.sui_rpc_url,
            headers=headers,
            json=payload,
        )
        return r.json()

    async def close(self):
        if self._owns_client:
            await self.http_client.aclose()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def __aenter__(self):
        return self
