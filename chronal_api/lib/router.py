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
        path: str,
        *args: Any,
        responses: dict[int | str, dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        responses_ = responses or dict()
        if self.api_routes_responses:
            responses_.update(self.api_routes_responses.get(path, {}))
        return super().add_api_route(path, *args, responses=responses_, **kwargs)
