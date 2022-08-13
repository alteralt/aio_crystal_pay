# noinspection PyPackageRequirements
import pytest
from pytest_mock import MockerFixture

from aio_crystal_pay import CrystalPay


wallet = CrystalPay("test_name", "test_secret1", "test_secret2")


@pytest.mark.asyncio
async def test_get_balance(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"balance": 0, "auth": "success"})
    assert {"balance": 0, "auth": "success"} == await wallet.get_balance()


@pytest.mark.asyncio
async def test_create_receipt(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success", "url": "https://test.com"})
    assert isinstance(await wallet.create_receipt(10, 10, currency="rub"), dict)


@pytest.mark.asyncio
async def test_check_receipt(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.check_receipt(10), dict)
