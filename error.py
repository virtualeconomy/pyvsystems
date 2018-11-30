class PyVSYSException(Exception):
    pass


class InvalidAddressException(PyVSYSException):
    pass


class InvalidParameterException(PyVSYSException):
    pass


class MissingPrivateKeyException(PyVSYSException):
    pass


class MissingPublicKeyException(PyVSYSException):
    pass


class MissingAddressException(PyVSYSException):
    pass


class InsufficientBalanceException(PyVSYSException):
    pass


class NetworkException(PyVSYSException):
    pass
