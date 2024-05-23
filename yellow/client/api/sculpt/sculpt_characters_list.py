from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.character_generation import CharacterGeneration
from ...models.error_message import ErrorMessage
from ...models.sculpt_characters_list_state_item import SculptCharactersListStateItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

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
        "url": "/api/sculpt/characters",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorMessage, List["CharacterGeneration"]]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CharacterGeneration.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorMessage, List["CharacterGeneration"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Response[Union[ErrorMessage, List["CharacterGeneration"]]]:
    """Lists already generated characters.

    Args:
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, List['CharacterGeneration']]]
    """

    kwargs = _get_kwargs(
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Optional[Union[ErrorMessage, List["CharacterGeneration"]]]:
    """Lists already generated characters.

    Args:
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, List['CharacterGeneration']]
    """

    return sync_detailed(
        client=client,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Response[Union[ErrorMessage, List["CharacterGeneration"]]]:
    """Lists already generated characters.

    Args:
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, List['CharacterGeneration']]]
    """

    kwargs = _get_kwargs(
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Optional[Union[ErrorMessage, List["CharacterGeneration"]]]:
    """Lists already generated characters.

    Args:
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, List['CharacterGeneration']]
    """

    return (
        await asyncio_detailed(
            client=client,
            state=state,
        )
    ).parsed
