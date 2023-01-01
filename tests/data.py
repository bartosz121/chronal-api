import uuid

import bcrypt
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from chronal_api.auth.models import User
from chronal_api.calendar.models import Calendar
from chronal_api.calendar_access.models import CalendarAccess, CalendarAccessRole

user_password = "passw0rd123!@#"
hashed_password = bcrypt.hashpw(user_password.encode("utf8"), bcrypt.gensalt()).decode(
    "utf8"
)

user_objs = [
    {
        "id": "404d2a4f-e6f4-4af5-be85-49eef8420216",
        "email": "user0@example.com",
        "hashed_password": hashed_password,
        "first_name": "user0 first name",
        "last_name": "user0 last name",
        "timezone": "Etc/UTC",
    },
    {
        "id": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
        "email": "user1@example.com",
        "hashed_password": hashed_password,
        "first_name": "user1 first name",
        "last_name": "user1 last name",
        "timezone": "Europe/Warsaw",
    },
    {
        "id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
        "email": "user2@example.com",
        "hashed_password": hashed_password,
        "first_name": "user2 first name",
        "last_name": "user2 last name",
        "timezone": "US/Michigan",
    },
    {
        "id": "a6da520a-3829-4248-ab3c-4b7818ffb165",
        "email": "user3@example.com",
        "hashed_password": hashed_password,
        "first_name": "user3 first name",
        "last_name": "user3 last name",
        "timezone": "Etc/UTC",
    },
    {
        "id": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
        "email": "user4@example.com",
        "hashed_password": hashed_password,
        "first_name": "user4 first name",
        "last_name": "user4 last name",
        "timezone": "Etc/UTC",
    },
    {
        "id": "e69197d8-0fe1-42e3-bf9e-6d4ae3afc716",
        "email": "user5@example.com",
        "hashed_password": hashed_password,
        "first_name": "user5 first name",
        "last_name": "user5 last name",
        "timezone": "Etc/UTC",
    },
    {
        "id": "f7e5f511-a4a3-49a3-8029-297f4e87e48b",
        "email": "SUPERUSER@example.com",
        "hashed_password": hashed_password,
        "first_name": "SUPERUSER",
        "last_name": "SUPERUSER",
        "timezone": "Etc/UTC",
        "is_superuser": True,
    },
]

# ONLY `INVITES` HERE, OWNER ACCESS OBJECTS ARE CREATED VIA SQLALCHEMY EVENT
calendar_objs = [
    {
        "id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "name": "Calendar #0",
        "description": "Calendar #0 description",
        "owner_id": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "name": "Calendar #1",
        "owner_id": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "97e98dab-f068-4a26-adae-1846441e4b13",
        "name": "Calendar #2",
        "description": "Calendar #2 description",
        "owner_id": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",
        "name": "Calendar #3",
        "description": "Calendar #3 description",
        "owner_id": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",  # user_objs[1]
    },
    {
        "id": "9deb3982-9636-4728-b875-8b65e48dedc5",
        "name": "Calendar #4",
        "owner_id": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",  # user_objs[1]
    },
    {
        "id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "name": "Calendar #5",
        "description": "Calendar #5 description",
        "owner_id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",  # user_objs[2]
    },
    {
        "id": "105f2f5d-300f-480d-828e-aa32945d01be",
        "name": "Calendar #6",
        "description": "Calendar #6 description",
        "owner_id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",  # user_objs[2]
    },
    {
        "id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "name": "Calendar #7",
        "owner_id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",  # user_objs[2]
    },
    {
        "id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "name": "Calendar #8",
        "owner_id": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",  # user_objs[4]
    },
]

calendar_access_objs = [
    {
        "id": "cd55ba7b-a858-42d2-81b0-cb9697759ebf",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",  # calendar_objs[0]
        "user_id": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",  # user_objs[1]
        "role": CalendarAccessRole.GUEST.value,
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "5511d663-dc61-430c-af55-4e0c999a7071",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",  # calendar_objs[0]
        "user_id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",  # user_objs[2]
        "role": CalendarAccessRole.STANDARD.value,
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "92173811-91e1-4028-980f-78a6534b639b",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",  # calendar_objs[0]
        "user_id": "a6da520a-3829-4248-ab3c-4b7818ffb165",  # user_objs[3]
        "role": CalendarAccessRole.MODERATOR.value,
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "02ad5a49-958d-40ed-8331-400b80c012ca",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",  # calendar_objs[0]
        "user_id": "e69197d8-0fe1-42e3-bf9e-6d4ae3afc716",  # user_objs[5]
        "role": CalendarAccessRole.MODERATOR.value,
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "4dbaa993-80ff-42cd-a36c-26d223e1be3e",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",  # calendar_objs[1]
        "user_id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",  # user_objs[2]
        "role": CalendarAccessRole.STANDARD.value,
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "f2de70a7-f2ac-463a-974f-82fcb8f9f172",
        "calendar_id": "97e98dab-f068-4a26-adae-1846441e4b13",  # calendar_objs[2]
        "user_id": "a6da520a-3829-4248-ab3c-4b7818ffb165",  # user_objs[3]
        "role": CalendarAccessRole.STANDARD.value,
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
    },
    {
        "id": "8b9d4e29-4412-4f87-8ed4-c7c87aa0fd90",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",  # calendar_objs[3]
        "user_id": "cbf24394-dd80-4f3c-a682-2089c5d98c20",  # user_objs[2]
        "role": CalendarAccessRole.MODERATOR.value,
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",  # user_objs[1]
    },
    {
        "id": "e405b295-cd2d-4a72-ab1c-84b835f801f6",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",  # calendar_objs[3]
        "user_id": "a6da520a-3829-4248-ab3c-4b7818ffb165",  # user_objs[3]
        "role": CalendarAccessRole.MODERATOR.value,
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",  # user_objs[1]
    },
    {
        "id": "e933e097-d26d-43a5-98ae-f5b3e19ea7db",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",  # calendar_objs[3]
        "user_id": "404d2a4f-e6f4-4af5-be85-49eef8420216",  # user_objs[0]
        "role": CalendarAccessRole.STANDARD.value,
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",  # user_objs[1]
    },
]


async def add_data(engine: AsyncEngine):
    conn = await engine.connect()
    session = AsyncSession(bind=conn)

    for user in user_objs:
        session.add(User(**user))

    for calendar in calendar_objs:
        session.add(Calendar(**calendar))

    for calendar_access in calendar_access_objs:
        session.add(CalendarAccess(**calendar_access))

    await session.commit()
    await session.close()
    await conn.close()


# used in user_client and superuser_client fixtures
AUTH_CLIENT_SUPERUSER = user_objs[6]
AUTH_CLIENT_USER0 = user_objs[0]
AUTH_CLIENT_USER1 = user_objs[1]
AUTH_CLIENT_USER2 = user_objs[2]
AUTH_CLIENT_USER3 = user_objs[3]
AUTH_CLIENT_USER4 = user_objs[4]
AUTH_CLIENT_USER5 = user_objs[5]

AUTH_CLIENT_USER0_CALENDARS = tuple(
    filter(lambda x: x["owner_id"] == AUTH_CLIENT_USER0["id"], calendar_objs)
)
AUTH_CLIENT_USER1_CALENDARS = tuple(
    filter(lambda x: x["owner_id"] == AUTH_CLIENT_USER1["id"], calendar_objs)
)

AUTH_CLIENT_USER2_CALENDARS = tuple(
    filter(lambda x: x["owner_id"] == AUTH_CLIENT_USER2["id"], calendar_objs)
)

AUTH_CLIENT_USER3_CALENDARS = tuple(
    filter(lambda x: x["owner_id"] == AUTH_CLIENT_USER3["id"], calendar_objs)
)

AUTH_CLIENT_USER4_CALENDARS = tuple(
    filter(lambda x: x["owner_id"] == AUTH_CLIENT_USER4["id"], calendar_objs)
)

AUTH_CLIENT_USER4_CALENDARS = tuple(
    filter(lambda x: x["owner_id"] == AUTH_CLIENT_USER5["id"], calendar_objs)
)

AUTH_CLIENT_USER0_ACCESS_LIST = tuple(
    filter(lambda x: x["user_id"] == AUTH_CLIENT_USER0["id"], calendar_access_objs)
)

AUTH_CLIENT_USER1_ACCESS_LIST = tuple(
    filter(lambda x: x["user_id"] == AUTH_CLIENT_USER1["id"], calendar_access_objs)
)

AUTH_CLIENT_USER2_ACCESS_LIST = tuple(
    filter(lambda x: x["user_id"] == AUTH_CLIENT_USER2["id"], calendar_access_objs)
)

AUTH_CLIENT_USER3_ACCESS_LIST = tuple(
    filter(lambda x: x["user_id"] == AUTH_CLIENT_USER3["id"], calendar_access_objs)
)

AUTH_CLIENT_USER4_ACCESS_LIST = tuple(
    filter(lambda x: x["user_id"] == AUTH_CLIENT_USER4["id"], calendar_access_objs)
)

AUTH_CLIENT_USER5_ACCESS_LIST = tuple(
    filter(lambda x: x["user_id"] == AUTH_CLIENT_USER5["id"], calendar_access_objs)
)

AUTH_CLIENT_USER0_ACCESS_CREATED_BY = tuple(
    filter(lambda x: x["created_by"] == AUTH_CLIENT_USER0["id"], calendar_access_objs)
)

AUTH_CLIENT_USER1_ACCESS_CREATED_BY = tuple(
    filter(lambda x: x["created_by"] == AUTH_CLIENT_USER1["id"], calendar_access_objs)
)
