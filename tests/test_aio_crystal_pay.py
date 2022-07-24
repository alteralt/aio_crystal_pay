# noinspection PyPackageRequirements
import pytest
from pytest_mock import MockerFixture

from aio_crystal_pay import CrystalPay


wallet = CrystalPay("test_name", "test_secret1", "test_secret2")


@pytest.mark.asyncio
async def test_get_balance(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"balance": 0, "auth": "success"})
    assert {"balance": 0, "auth": "success"} == await wallet.get_balance()
