# noinspection PyPackageRequirements
import pytest
from pytest_mock import MockerFixture

import aio_crystal_pay

wallet = aio_crystal_pay.CrystalPay("test_name", "test_secret1", "test_secret2")


@pytest.mark.asyncio
async def test_get_balance(mocker: MockerFixture):
    mocker.patch(
        "aiohttp.ClientResponse.json", return_value={"balance": 0, "auth": "success"}
    )
    assert {"balance": 0, "auth": "success"} == await wallet.get_balance()


@pytest.mark.asyncio
async def test_create_receipt(mocker: MockerFixture):
    mocker.patch(
        "aiohttp.ClientResponse.json",
        return_value={"auth": "success", "url": "https://test.com"},
    )
    assert isinstance(await wallet.create_receipt(10, 10, currency="rub"), dict)


@pytest.mark.asyncio
async def test_check_receipt(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.check_receipt(10), dict)


@pytest.mark.asyncio
async def test_create_withdraw(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.create_withdraw(10, "rub", "test_wallet"), dict)


@pytest.mark.asyncio
async def test_check_withdraw(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.check_withdraw(10), dict)


@pytest.mark.asyncio
async def test_p2p_transfer(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.p2p_transfer("test_login", 10, "rub"), dict)


@pytest.mark.asyncio
async def test_create_voucher(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(
        await wallet.create_voucher(10, "rub", comment="test_comment"), dict
    )


@pytest.mark.asyncio
async def test_voucher_info(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.voucher_info("test_code"), dict)


@pytest.mark.asyncio
async def test_activate_voucher(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "success"})
    assert isinstance(await wallet.activate_voucher("test_code"), dict)


@pytest.mark.asyncio
async def test_raise_auth_error(mocker: MockerFixture):
    mocker.patch("aiohttp.ClientResponse.json", return_value={"auth": "error"})
    with pytest.raises(aio_crystal_pay.exceptions.AuthorizationError):
        await wallet.get_balance()


def test_generate_payment_hash():
    assert isinstance(wallet.generate_payment_hash(1, "test"), str)
