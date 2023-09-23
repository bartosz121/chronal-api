from chronal_api.lib.service.exceptions import ServiceException


class EmailAlreadyExists(ServiceException):
    ...


class UserNotFound(ServiceException):
    ...
