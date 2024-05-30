from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_message import ErrorMessage
from ...models.paginated_character_retopology_list import PaginatedCharacterRetopologyList
from ...models.retopology_characters_list_state_item import RetopologyCharactersListStateItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, List[RetopologyCharactersListStateItem]] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["page_size"] = page_size

    json_state: Union[Unset, List[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/retopology/characters",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorMessage, PaginatedCharacterRetopologyList]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginatedCharacterRetopologyList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorMessage, PaginatedCharacterRetopologyList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, List[RetopologyCharactersListStateItem]] = UNSET,
) -> Response[Union[ErrorMessage, PaginatedCharacterRetopologyList]]:
    """Lists launched retopologies. Can be filtered based on their state.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, List[RetopologyCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, PaginatedCharacterRetopologyList]]
    """

    kwargs = _get_kwargs(
        page=page,
        page_size=page_size,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, List[RetopologyCharactersListStateItem]] = UNSET,
) -> Optional[Union[ErrorMessage, PaginatedCharacterRetopologyList]]:
    """Lists launched retopologies. Can be filtered based on their state.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, List[RetopologyCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, PaginatedCharacterRetopologyList]
    """

    return sync_detailed(
        client=client,
        page=page,
        page_size=page_size,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, List[RetopologyCharactersListStateItem]] = UNSET,
) -> Response[Union[ErrorMessage, PaginatedCharacterRetopologyList]]:
    """Lists launched retopologies. Can be filtered based on their state.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, List[RetopologyCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, PaginatedCharacterRetopologyList]]
    """

    kwargs = _get_kwargs(
        page=page,
        page_size=page_size,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, List[RetopologyCharactersListStateItem]] = UNSET,
) -> Optional[Union[ErrorMessage, PaginatedCharacterRetopologyList]]:
    """Lists launched retopologies. Can be filtered based on their state.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, List[RetopologyCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, PaginatedCharacterRetopologyList]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            page_size=page_size,
            state=state,
        )
    ).parsed
