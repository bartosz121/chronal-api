class RepositoryException(Exception):
    """Base exception for repository errors"""


class Conflict(RepositoryException):
    """Raised when a conflict is detected"""


class NotFound(RepositoryException):
    """Raised when a resource is not found"""
