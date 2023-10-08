from typing import Any

from fastapi import APIRouter as APIRouter_


class APIRouter(APIRouter_):
    def __init__(
        self,
        *args: Any,
        api_routes_responses: dict[str, dict[int | str, dict[str, Any]]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.api_routes_responses = api_routes_responses

    def add_api_route(
        self,
        *args: Any,
        name: str | None = None,
        responses: dict[int | str, dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        responses_new = responses or dict()
        if self.api_routes_responses and name:
            responses_new.update(self.api_routes_responses.get(name, {}))
        return super().add_api_route(*args, name=name, responses=responses_new, **kwargs)
