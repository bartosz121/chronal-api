from chronal_api.core.abc import UUID, BaseService

from .models import Event
from .schemas import EventCreate, EventRead, EventUpdate


class EventService(BaseService[Event, EventCreate, EventUpdate]):
    async def get_events_created_by(self, user_id: UUID) -> list[Event]:
        user_events = await self.get(created_by=user_id)
        return user_events

    async def get_events_for_calendar(self, calendar_id: UUID) -> list[Event]:
        events = await self.get(calendar_id=calendar_id)
        return events
