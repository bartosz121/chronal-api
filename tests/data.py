import bcrypt
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from chronal_api.auth.models import User
from chronal_api.calendar.models import Calendar
from chronal_api.calendar_access.models import CalendarAccess, CalendarAccessRole
from chronal_api.events.models import Event

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

event_objs = [
    {
        "id": "5266fbaf-97e2-4e9a-83d4-e8a40e6e1325",
        "title": "Event #0",
        "description": "Event #0 description",
        "start_dt": DateTime(2137, 11, 17, 11, 29, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 11, 17, 23, 29, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Baghdad",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "2b903608-b6ee-494c-be2e-978ac5f3264e",
        "title": "Event #1",
        "description": "Event #1 description",
        "start_dt": DateTime(2137, 12, 17, 13, 31, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 18, 13, 31, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Mogadishu",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
    },
    {
        "id": "e8dfd16b-0c2a-4e04-a6e1-d5cdcc9bd911",
        "title": "Event #2",
        "description": "Event #2 description",
        "start_dt": DateTime(2137, 3, 24, 17, 9, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 3, 25, 12, 9, 0, tzinfo=Timezone("UTC")),
        "timezone": "Etc/GMT+8",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "d8b2dde3-10ba-42df-9abb-d865568e0c0e",
        "title": "Event #3",
        "description": "Event #3 description",
        "start_dt": DateTime(2137, 10, 2, 19, 55, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 10, 3, 11, 55, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Adak",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "0affd1ac-27ac-4773-99c9-0a177968f290",
        "title": "Event #4",
        "description": "Event #4 description",
        "start_dt": DateTime(2137, 11, 6, 15, 47, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 11, 7, 2, 47, 0, tzinfo=Timezone("UTC")),
        "timezone": "Eire",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "04ce23f7-8a6d-4228-bb57-8441239a3392",
        "title": "Event #5",
        "description": "Event #5 description",
        "start_dt": DateTime(2137, 11, 9, 21, 41, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 11, 9, 22, 0, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Indiana/Vevay",
        "calendar_id": "105f2f5d-300f-480d-828e-aa32945d01be",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "75c45dc1-53d3-4493-b045-725906f4f494",
        "title": "Event #6",
        "description": "Event #6 description",
        "start_dt": DateTime(2137, 12, 5, 12, 3, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 5, 12, 34, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Srednekolymsk",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "f2514c81-01bf-4f5e-860c-23b5b1cdf94b",
        "title": "Event #7",
        "description": "Event #7 description",
        "start_dt": DateTime(2137, 6, 9, 10, 14, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 6, 11, 10, 14, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Nipigon",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "f18802f4-f8f8-49d7-9e01-4d1108237f70",
        "title": "Event #8",
        "description": "Event #8 description",
        "start_dt": DateTime(2137, 3, 7, 16, 48, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 3, 8, 13, 48, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Kathmandu",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "1864f66b-b4d2-4c5d-8400-a144a00175bf",
        "title": "Event #9",
        "description": "Event #9 description",
        "start_dt": DateTime(2137, 10, 19, 16, 12, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 10, 23, 16, 12, 0, tzinfo=Timezone("UTC")),
        "timezone": "Singapore",
        "calendar_id": "9deb3982-9636-4728-b875-8b65e48dedc5",
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
    },
    {
        "id": "10204a8d-c8da-4087-86b7-571a33238637",
        "title": "Event #10",
        "description": "Event #10 description",
        "start_dt": DateTime(2137, 7, 24, 22, 48, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 7, 29, 22, 48, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Djibouti",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "0eb909e0-ca33-4241-9447-923bd107a381",
        "title": "Event #11",
        "description": "Event #11 description",
        "start_dt": DateTime(2137, 1, 15, 10, 38, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 24, 10, 38, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Argentina/Ushuaia",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "0609a7d0-5293-4c97-a737-62cb2291eae0",
        "title": "Event #12",
        "description": "Event #12 description",
        "start_dt": DateTime(2137, 4, 3, 11, 14, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 4, 3, 11, 16, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Boa_Vista",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "bbd24910-f704-4259-934e-620e9a392249",
        "title": "Event #13",
        "description": "Event #13 description",
        "start_dt": DateTime(2137, 6, 16, 13, 26, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 6, 16, 13, 40, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Puerto_Rico",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "7e7f832f-6abf-4d40-86c8-5e2863dda06b",
        "title": "Event #14",
        "description": "Event #14 description",
        "start_dt": DateTime(2137, 1, 10, 18, 54, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 17, 18, 54, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Algiers",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "0330a963-fa4b-4a65-bafd-d0e42d5ccc8c",
        "title": "Event #15",
        "description": "Event #15 description",
        "start_dt": DateTime(2137, 4, 10, 14, 48, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 4, 10, 14, 57, 0, tzinfo=Timezone("UTC")),
        "timezone": "Universal",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "d0549bba-fcf6-416e-a0eb-1dccd4b22526",
        "title": "Event #16",
        "description": "Event #16 description",
        "start_dt": DateTime(2137, 12, 7, 16, 39, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 17, 16, 39, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Irkutsk",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "5b07fb40-fa76-4123-9609-32b4675df7b9",
        "title": "Event #17",
        "description": "Event #17 description",
        "start_dt": DateTime(2137, 7, 2, 12, 15, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 7, 3, 11, 15, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Khartoum",
        "calendar_id": "105f2f5d-300f-480d-828e-aa32945d01be",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "423ee8b7-9454-481a-9dee-a4e621d1255c",
        "title": "Event #18",
        "description": "Event #18 description",
        "start_dt": DateTime(2137, 7, 10, 18, 36, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 7, 16, 18, 36, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/New_York",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "a3245569-e31b-4f63-9ddf-2472f323162e",
        "title": "Event #19",
        "description": "Event #19 description",
        "start_dt": DateTime(2137, 4, 27, 14, 28, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 4, 28, 14, 28, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Bahia",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "3cf0f61d-1e23-4180-8c6e-d4c2ab7b7083",
        "title": "Event #20",
        "description": "Event #20 description",
        "start_dt": DateTime(2137, 3, 17, 12, 9, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 3, 17, 12, 34, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Libreville",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
    },
    {
        "id": "677e1c4e-9a29-4c0d-a639-ab4e535f99b1",
        "title": "Event #21",
        "description": "Event #21 description",
        "start_dt": DateTime(2137, 12, 8, 19, 34, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 11, 19, 34, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Chungking",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "f6eccf51-a445-440b-8862-97c24ede5177",
        "title": "Event #22",
        "description": "Event #22 description",
        "start_dt": DateTime(2137, 4, 27, 12, 53, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 4, 27, 21, 53, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Toronto",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "0036f177-9f08-475e-94f2-9308839baf2c",
        "title": "Event #23",
        "description": "Event #23 description",
        "start_dt": DateTime(2137, 1, 28, 13, 32, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 28, 14, 4, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/North_Dakota/Center",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "33190576-15f0-4190-81c3-83cd9967010b",
        "title": "Event #24",
        "description": "Event #24 description",
        "start_dt": DateTime(2137, 1, 16, 11, 47, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 19, 11, 47, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Nassau",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "00778ebb-7d5a-499f-8a0c-471b3c7a0880",
        "title": "Event #25",
        "description": "Event #25 description",
        "start_dt": DateTime(2137, 9, 8, 17, 18, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 9, 8, 17, 19, 0, tzinfo=Timezone("UTC")),
        "timezone": "Japan",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "3a0299fd-b6d3-4fb0-bbd9-ce9c2f4448d4",
        "title": "Event #26",
        "description": "Event #26 description",
        "start_dt": DateTime(2137, 12, 2, 22, 1, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 3, 4, 1, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Bahrain",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "e90851fd-cff9-4838-bb94-d08a05d57cbd",
        "title": "Event #27",
        "description": "Event #27 description",
        "start_dt": DateTime(2137, 4, 8, 17, 20, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 4, 8, 18, 0, 0, tzinfo=Timezone("UTC")),
        "timezone": "Europe/Budapest",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "7b5bd394-c91d-4908-9423-c6124934dc8b",
        "title": "Event #28",
        "description": "Event #28 description",
        "start_dt": DateTime(2137, 8, 20, 14, 2, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 8, 20, 14, 57, 0, tzinfo=Timezone("UTC")),
        "timezone": "GMT",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
    },
    {
        "id": "f4d8e170-6ff1-4908-a01c-170c26c96646",
        "title": "Event #29",
        "description": "Event #29 description",
        "start_dt": DateTime(2137, 9, 17, 18, 8, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 9, 18, 8, 8, 0, tzinfo=Timezone("UTC")),
        "timezone": "Indian/Kerguelen",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "92637bbb-8daa-4cc3-a1a3-9691a212bf98",
        "title": "Event #30",
        "description": "Event #30 description",
        "start_dt": DateTime(2137, 10, 5, 10, 53, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 10, 13, 10, 53, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Maceio",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "f4a01e8c-60e9-4a61-be19-34931e1e8260",
        "title": "Event #31",
        "description": "Event #31 description",
        "start_dt": DateTime(2137, 7, 23, 10, 4, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 7, 23, 10, 6, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Dar_es_Salaam",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "ceb1fe55-9d2e-4938-b992-c4350f388a3f",
        "title": "Event #32",
        "description": "Event #32 description",
        "start_dt": DateTime(2137, 12, 3, 16, 45, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 12, 16, 45, 0, tzinfo=Timezone("UTC")),
        "timezone": "ROK",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "8bad80d8-fd9a-467c-929c-41b45c49c593",
        "title": "Event #33",
        "description": "Event #33 description",
        "start_dt": DateTime(2137, 1, 5, 11, 15, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 5, 12, 7, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Accra",
        "calendar_id": "9deb3982-9636-4728-b875-8b65e48dedc5",
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
    },
    {
        "id": "84af6e76-9bc5-4521-907c-8c5f021ad49a",
        "title": "Event #34",
        "description": "Event #34 description",
        "start_dt": DateTime(2137, 1, 12, 12, 18, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 21, 12, 18, 0, tzinfo=Timezone("UTC")),
        "timezone": "Pacific/Pago_Pago",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "27035ef6-43ed-4e07-983b-5fd83c24c07a",
        "title": "Event #35",
        "description": "Event #35 description",
        "start_dt": DateTime(2137, 4, 11, 11, 7, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 4, 11, 23, 7, 0, tzinfo=Timezone("UTC")),
        "timezone": "HST",
        "calendar_id": "97e98dab-f068-4a26-adae-1846441e4b13",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "1e1b6b29-333d-4409-8e07-09d932f3e295",
        "title": "Event #36",
        "description": "Event #36 description",
        "start_dt": DateTime(2137, 3, 5, 19, 32, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 3, 5, 20, 8, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Dawson_Creek",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "976ce5a6-b428-4920-9f4d-1350472ad7bd",
        "title": "Event #37",
        "description": "Event #37 description",
        "start_dt": DateTime(2137, 12, 4, 13, 38, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 14, 13, 38, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Asmara",
        "calendar_id": "105f2f5d-300f-480d-828e-aa32945d01be",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "aa24c2d3-0685-4fef-8765-fd1647ebd3c9",
        "title": "Event #38",
        "description": "Event #38 description",
        "start_dt": DateTime(2137, 5, 1, 15, 17, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 5, 1, 16, 17, 0, tzinfo=Timezone("UTC")),
        "timezone": "Africa/Lusaka",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "bffb8c09-1b1c-4ba8-b657-03e7d3d276cb",
        "title": "Event #39",
        "description": "Event #39 description",
        "start_dt": DateTime(2137, 2, 18, 20, 47, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 2, 24, 20, 47, 0, tzinfo=Timezone("UTC")),
        "timezone": "Etc/UCT",
        "calendar_id": "d4c12715-26e5-4851-9e5e-0b88e06452b6",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "b556e72a-904b-4166-a66a-4925f1607ce1",
        "title": "Event #40",
        "description": "Event #40 description",
        "start_dt": DateTime(2137, 11, 26, 16, 52, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 11, 26, 19, 52, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Caracas",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "2acd415c-abae-48b0-890f-9e9cce2cbf8c",
        "title": "Event #41",
        "description": "Event #41 description",
        "start_dt": DateTime(2137, 1, 28, 17, 30, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 1, 28, 18, 2, 0, tzinfo=Timezone("UTC")),
        "timezone": "Australia/Melbourne",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "d327b03e-ab18-4288-83a4-c2cb98cd6240",
        "title": "Event #42",
        "description": "Event #42 description",
        "start_dt": DateTime(2137, 8, 1, 20, 46, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 8, 1, 23, 46, 0, tzinfo=Timezone("UTC")),
        "timezone": "America/Goose_Bay",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "835cc7f9-aa79-474b-a373-e98a833fbd48",
        "title": "Event #43",
        "description": "Event #43 description",
        "start_dt": DateTime(2137, 9, 16, 17, 43, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 9, 17, 11, 43, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Dhaka",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "62be5435-76c0-4b4b-b175-9590f0bf9e06",
        "title": "Event #44",
        "description": "Event #44 description",
        "start_dt": DateTime(2137, 5, 10, 19, 37, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 5, 11, 8, 37, 0, tzinfo=Timezone("UTC")),
        "timezone": "Europe/Sofia",
        "calendar_id": "b179143f-23e7-468e-88c3-03b7d9c47e43",
        "created_by": "404d2a4f-e6f4-4af5-be85-49eef8420216",
    },
    {
        "id": "6a5fe418-221e-43a0-9888-e97a7128e366",
        "title": "Event #45",
        "description": "Event #45 description",
        "start_dt": DateTime(2137, 2, 9, 12, 22, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 2, 10, 4, 22, 0, tzinfo=Timezone("UTC")),
        "timezone": "Europe/Prague",
        "calendar_id": "ef32e43f-d8b5-4592-b2e2-3e55b643b81a",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "6779d322-c1e9-43ab-8bc5-fea3738099f5",
        "title": "Event #46",
        "description": "Event #46 description",
        "start_dt": DateTime(2137, 8, 6, 21, 28, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 8, 6, 21, 29, 0, tzinfo=Timezone("UTC")),
        "timezone": "Europe/Mariehamn",
        "calendar_id": "67399b6b-46a6-420d-bbe3-2a5d4a539426",
        "created_by": "d6607c8a-01a9-460f-ac1a-0d0000d2f242",
    },
    {
        "id": "64a493f8-a873-445c-bd47-a76648ccfa05",
        "title": "Event #47",
        "description": "Event #47 description",
        "start_dt": DateTime(2137, 9, 29, 20, 8, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 9, 30, 17, 8, 0, tzinfo=Timezone("UTC")),
        "timezone": "Asia/Bangkok",
        "calendar_id": "15e7f40b-686b-4885-80cc-6cdd77633b9e",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "5cf0c7cd-3c2f-4ace-859d-0819902afffb",
        "title": "Event #48",
        "description": "Event #48 description",
        "start_dt": DateTime(2137, 12, 14, 15, 50, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 12, 15, 1, 50, 0, tzinfo=Timezone("UTC")),
        "timezone": "Indian/Comoro",
        "calendar_id": "105f2f5d-300f-480d-828e-aa32945d01be",
        "created_by": "cbf24394-dd80-4f3c-a682-2089c5d98c20",
    },
    {
        "id": "6f53cd9a-fabc-4a36-abc2-78a5ad894123",
        "title": "Event #49",
        "description": "Event #49 description",
        "start_dt": DateTime(2137, 8, 23, 19, 4, 0, tzinfo=Timezone("UTC")),
        "end_dt": DateTime(2137, 8, 25, 19, 4, 0, tzinfo=Timezone("UTC")),
        "timezone": "Singapore",
        "calendar_id": "ac19046a-8473-4063-9df3-3dbb6f7393cf",
        "created_by": "6a7acf60-f3c4-435a-8cd9-b97604c948fa",
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

    for event in event_objs:
        session.add(Event(**event))

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

EVENTS_BY_USER_ID: dict[str, list[dict[str, str]]] = {
    user["id"]: list(filter(lambda x: x["created_by"] == user["id"], event_objs))
    for user in user_objs
}

EVENTS_BY_CALENDAR_ID = {
    calendar["id"]: list(
        filter(lambda x: x["calendar_id"] == calendar["id"], event_objs)
    )
    for calendar in calendar_objs
}

CALENDAR_IDS_BY_USER_ID = {
    user["id"]: list(
        map(
            lambda y: y["id"],
            filter(lambda x: x["owner_id"] == user["id"], calendar_objs),
        )
    )
    for user in user_objs
}

USER_ACCESS_CALENDAR_IDS_BY_USER_ID: dict[str, list[str]] = {
    user["id"]: list(
        map(
            lambda y: y["calendar_id"],
            filter(lambda x: x["user_id"] == user["id"], calendar_access_objs),
        )
    )
    for user in user_objs
}
