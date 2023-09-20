from chronal_api.lib.service.exceptions import ServiceException

# Service exceptions


class WrongPassword(ServiceException):
    ...


class InvalidAccessToken(ServiceException):
    ...


class ExpiredAccessToken(ServiceException):
    ...
