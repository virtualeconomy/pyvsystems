class PyVeeException(Exception):
    pass


class InvalidAddressException(PyVeeException):
    pass


class InvalidParameterException(PyVeeException):
    pass


class MissingPrivateKeyException(PyVeeException):
    pass


class MissingPublicKeyException(PyVeeException):
    pass


class MissingAddressException(PyVeeException):
    pass


class InsufficientBalanceException(PyVeeException):
    pass


class NetworkException(PyVeeException):
    pass
