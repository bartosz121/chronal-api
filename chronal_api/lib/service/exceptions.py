class ServiceException(Exception):
    """Base exception for service errors"""


class ItemNotFound(ServiceException):
    ...
