# noinspection PyPackageRequirements
import pytest
from pytest_mock import MockerFixture

import aio_crystal_pay

wallet = aio_crystal_pay.CrystalPay("test_name", "test_secret1", "test_secret2")


@pytest.mark.asyncio
async def test_get_balance(mocker: MockerFixture):
    mocker.patch(
        "aiohttp.ClientResponse.json", return_value={"balances": [], "error": False}
    )
    assert [] == await wallet.get_balance()


@pytest.mark.asyncio
async def test_raise_auth_error(mocker: MockerFixture):
    mocker.patch(
        "aiohttp.ClientResponse.json",
        return_value={"error": True, "errors": ["Invalid auth credentials"]},
    )
    with pytest.raises(aio_crystal_pay.exceptions.AuthorizationError):
        await wallet.get_balance()


def test_generate_payment_hash():
    assert isinstance(wallet.generate_payment_hash(1), str)


@pytest.mark.asyncio
async def test_create_receipt(mocker: MockerFixture):
    mocker.patch(
        "aiohttp.ClientResponse.json",
        return_value={"error": False, "url": "https://test.com"},
    )
    assert isinstance(await wallet.create_invoice(10, 10, currency="rub"), dict)


@pytest.mark.asyncio
async def test_request(mocker: MockerFixture):
    mocker.patch(
        "aiohttp.ClientResponse.json",
        return_value={"error": True, "errors": ["test_error"]},
    )

    with pytest.raises(aio_crystal_pay.exceptions.BaseCrystalPayException):
        await wallet._request("post", "test")
