import httpx
from types import TracebackType
from typing import Optional, Type
from dataclasses import dataclass
from sui_gas_pool_sdk.exceptions import GasReservationDurationTooLongException


@dataclass
class GasCoin:
    object_id: str
    version: int
    digest: str


@dataclass
class GasReservation:
    sponsor_address: str
    reservation_id: int
    gas_coins: list[GasCoin]


@dataclass
class SponsoredTxResponse:
    tx_digest: str


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

    async def sponsor_and_execute_tx(
        self,
        tx_bytes: str,
        gas_budget: int,
        reserve_duration_secs: int,
    ) -> str:
        """
        Reserve gas and submit a transaction to a sui-gas-pool service and return the transaction digest.

        Args:
            tx_bytes: The transaction bytes to execute.
            gas_budget: The gas budget for the transaction.
            reserve_duration_secs: The duration to reserve gas for.

        Returns:
            The transaction digest.
        """
        gas_reservation = await self.reserve_gas(
            gas_budget=gas_budget,
            reserve_duration_secs=reserve_duration_secs,
        )
        tx_digest = await self.execute_tx(
            tx_bytes=tx_bytes,
            reservation_id=gas_reservation.reservation_id,
        )
        return tx_digest

    async def execute_tx(
        self,
        tx_bytes: str,
        reservation_id: int,
        user_sig: str,
    ) -> str:
        """
        Submit a transaction to a sui-gas-pool service.

        Args:
            tx_bytes: The transaction bytes to execute.
            reservation_id: The reservation ID to use for the transaction.
            user_sig: The user signature for the transaction.

        Returns:
            The transaction digest.
        """
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
        r.raise_for_status()
        tx_digest = r.json()["effects"]["transactionDigest"]
        return tx_digest

    async def reserve_gas(
        self,
        gas_budget: int,
        reserve_duration_secs: int,
    ) -> GasReservation:
        """
        Reserve gas for a transaction.

        Args:
            gas_budget: The gas budget for the transaction.
            reserve_duration_secs: The duration to reserve gas for.

        Returns:
            A GasReservation object.
        """
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
        r.raise_for_status()
        return GasReservation(
            sponsor_address=r.json()["result"]["sponsor_address"],
            reservation_id=r.json()["result"]["reservation_id"],
            gas_coins=[
                GasCoin(
                    object_id=coin["objectId"],
                    version=coin["version"],
                    digest=coin["digest"],
                )
                for coin in r.json()["result"]["gas_coins"]
            ],
        )

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
