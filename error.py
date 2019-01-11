class PyVException(Exception):
    pass


class InvalidAddressException(PyVException):
    pass


class InvalidParameterException(PyVException):
    pass


class MissingPrivateKeyException(PyVException):
    pass


class MissingPublicKeyException(PyVException):
    pass


class MissingAddressException(PyVException):
    pass


class InsufficientBalanceException(PyVException):
    pass


class NetworkException(PyVException):
    pass
