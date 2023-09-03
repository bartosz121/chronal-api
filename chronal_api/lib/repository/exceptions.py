class RepositoryException(Exception):
    """Base exception for repository errors"""


class ConflictError(RepositoryException):
    """Raised when a conflict is detected"""


class NotFoundError(RepositoryException):
    """Raised when a resource is not found"""
