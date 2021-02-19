
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


class InvalidStatus(PyVException):
    pass


class MissingContractIdException(PyVException):
    pass


class MissingTokenIdException(PyVException):
    pass

class InvalidContractException(PyVException):
    pass


def set_throw_on_error(throw=True):
    global THROW_EXCEPTION_ON_ERROR
    THROW_EXCEPTION_ON_ERROR = throw


def throw_error(msg, exception=PyVException):
    global THROW_EXCEPTION_ON_ERROR
    if THROW_EXCEPTION_ON_ERROR:
        raise exception(msg)
