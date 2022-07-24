import hashlib
import aiohttp

from . import exceptions


class CrystalPay:
    default_url = "https://api.crystalpay.ru/v1/"

    def __init__(self, name, secret1, secret2):
        self.secret1 = secret1
        self.secret2 = secret2
        self.name = name

    def get_params(self, **kwargs):
        params = {
            "s": self.secret1,
            "n": self.name,
        }
        params.update(**{key: value for key, value in kwargs.items() if value is not None})
        return params

    async def _request(self, method, params):
        async with aiohttp.ClientSession() as session:
            response = await session.request(method, self.default_url, params=params)
            await response.read()

        await self._handle_response(response)
        return await response.json()

    @classmethod
    async def _handle_response(cls, response):
        if "error" == (await response.json())["auth"]:
            raise exceptions.AuthorizationError('Check SECRET1, SECRET2 and name cash register', 'auth_error')

    @staticmethod
    def _create_secret_hash(*args):
        return hashlib.md5('@'.join([str(elem) for elem in args]).encode()).hexdigest()

    async def create_receipt(self, amount, lifetime, extra=None, callback=None, redirect=None, currency=None):
        operation = 'receipt-create'
        params = self.get_params(
            o=operation,
            amount=amount,
            lifetime=lifetime,
            extra=extra or None,
            callback=callback or None,
            redirect=redirect or None
        )

        if currency:
            r = await self._request('GET', params)
            r['url'] = r['url'] + '&m=' + currency
            return r
        else:
            return await self._request('GET', params)

    async def check_receipt(self, receipt_id):
        return await self._request('GET', self.get_params(o='receipt-check', i=receipt_id))

    async def get_balance(self):
        return await self._request('GET', self.get_params(o='balance'))

    async def create_withdraw(self, amount, currency, wallet, callback=None):
        operation = 'withdraw'
        withdraw_secret = self._create_secret_hash(wallet, amount, self.secret2)
        params = self.get_params(
            o=operation,
            secret=withdraw_secret,
            amount=amount,
            wallet=wallet,
            currency=currency,
            callback=callback or None
        )
        return await self._request('GET', params)

    async def check_withdraw(self, withdraw_id):
        operation = 'withdraw-status'
        params = self.get_params(o=operation, i=withdraw_id)
        return await self._request('GET', params)

    async def p2p_transfer(self, login, amount, currency):
        operation = 'p2p-transfer'
        p2p_secret = self._create_secret_hash(currency, amount, login, self.secret2)
        params = self.get_params(o=operation, secret=p2p_secret, login=login, amount=amount, currency=currency)
        return await self._request('GET', params)

    async def create_voucher(self, amount, currency, comment=None):
        operation = 'voucher-create'
        voucher_secret = self._create_secret_hash(currency, amount, self.secret2)
        if comment:
            params = self.get_params(o=operation, secret=voucher_secret, comment=comment)
        else:
            params = self.get_params(o=operation, secret=voucher_secret)
        return await self._request('GET', params)

    async def voucher_info(self, voucher_code):
        operation = 'voucher-info'
        params = self.get_params(o=operation, code=voucher_code)
        return await self._request('GET', params)

    async def activate_voucher(self, voucher_code):
        return await self._request('GET', self.get_params(o='voucher-activate', code=voucher_code))
