import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_message import ErrorMessage
from ...models.paginated_character_generation_list import PaginatedCharacterGenerationList
from ...models.sculpt_characters_list_gender_item import SculptCharactersListGenderItem
from ...models.sculpt_characters_list_state_item import SculptCharactersListStateItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    end_date: Union[Unset, datetime.date] = UNSET,
    gender: Union[Unset, List[SculptCharactersListGenderItem]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    json_gender: Union[Unset, List[str]] = UNSET
    if not isinstance(gender, Unset):
        json_gender = []
        for gender_item_data in gender:
            gender_item = gender_item_data.value
            json_gender.append(gender_item)

    params["gender"] = json_gender

    params["page"] = page

    params["page_size"] = page_size

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

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
) -> Optional[Union[ErrorMessage, PaginatedCharacterGenerationList]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginatedCharacterGenerationList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorMessage, PaginatedCharacterGenerationList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    end_date: Union[Unset, datetime.date] = UNSET,
    gender: Union[Unset, List[SculptCharactersListGenderItem]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Response[Union[ErrorMessage, PaginatedCharacterGenerationList]]:
    """Lists already generated characters.

    Args:
        end_date (Union[Unset, datetime.date]):
        gender (Union[Unset, List[SculptCharactersListGenderItem]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, PaginatedCharacterGenerationList]]
    """

    kwargs = _get_kwargs(
        end_date=end_date,
        gender=gender,
        page=page,
        page_size=page_size,
        start_date=start_date,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    end_date: Union[Unset, datetime.date] = UNSET,
    gender: Union[Unset, List[SculptCharactersListGenderItem]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Optional[Union[ErrorMessage, PaginatedCharacterGenerationList]]:
    """Lists already generated characters.

    Args:
        end_date (Union[Unset, datetime.date]):
        gender (Union[Unset, List[SculptCharactersListGenderItem]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, PaginatedCharacterGenerationList]
    """

    return sync_detailed(
        client=client,
        end_date=end_date,
        gender=gender,
        page=page,
        page_size=page_size,
        start_date=start_date,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    end_date: Union[Unset, datetime.date] = UNSET,
    gender: Union[Unset, List[SculptCharactersListGenderItem]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Response[Union[ErrorMessage, PaginatedCharacterGenerationList]]:
    """Lists already generated characters.

    Args:
        end_date (Union[Unset, datetime.date]):
        gender (Union[Unset, List[SculptCharactersListGenderItem]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, PaginatedCharacterGenerationList]]
    """

    kwargs = _get_kwargs(
        end_date=end_date,
        gender=gender,
        page=page,
        page_size=page_size,
        start_date=start_date,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    end_date: Union[Unset, datetime.date] = UNSET,
    gender: Union[Unset, List[SculptCharactersListGenderItem]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, List[SculptCharactersListStateItem]] = UNSET,
) -> Optional[Union[ErrorMessage, PaginatedCharacterGenerationList]]:
    """Lists already generated characters.

    Args:
        end_date (Union[Unset, datetime.date]):
        gender (Union[Unset, List[SculptCharactersListGenderItem]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, List[SculptCharactersListStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, PaginatedCharacterGenerationList]
    """

    return (
        await asyncio_detailed(
            client=client,
            end_date=end_date,
            gender=gender,
            page=page,
            page_size=page_size,
            start_date=start_date,
            state=state,
        )
    ).parsed
