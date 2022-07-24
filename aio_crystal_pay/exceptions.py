class BaseCrystalPayException(Exception):
    def __init__(self, message, error):
        super().__init__(message)
        self.error = error


class AuthorizationError(BaseCrystalPayException):
    pass
