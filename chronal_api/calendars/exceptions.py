from enum import StrEnum

from chronal_api.lib.service import exceptions as service_exceptions


class TitleNotUnique(service_exceptions.ServiceException):
    ...


class HTTPError(StrEnum):
    TITLE_NOT_UNIQUE = "Calendar with this title already exists"
    CALENDAR_NOT_FOUND = "Calendar not found"
    FORBIDDEN = "You don't have access to this calendar"
