from enum import StrEnum

from chronal_api.lib.service.exceptions import ServiceException


class EmailAlreadyExists(ServiceException):
    ...


class UserNotFound(ServiceException):
    ...


class HTTPError(StrEnum):
    EMAIL_ALREADY_IN_USE = "Email already in use"
    EMAIL_NOT_FOUND = "User with this email does not exist"
    WRONG_PASSWORD = "Wrong password"
