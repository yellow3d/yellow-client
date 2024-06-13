from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.character_generation_status import CharacterGenerationStatus
from ...models.error_message import ErrorMessage
from ...types import UNSET, Response


def _get_kwargs(
    *,
    generation_id: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["generation_id"] = generation_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/sculpt/characters/status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CharacterGenerationStatus, ErrorMessage]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorMessage.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.OK:
        response_200 = CharacterGenerationStatus.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CharacterGenerationStatus, ErrorMessage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    generation_id: str,
) -> Response[Union[CharacterGenerationStatus, ErrorMessage]]:
    """Fetches the progress of the generation.

    Args:
        generation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CharacterGenerationStatus, ErrorMessage]]
    """

    kwargs = _get_kwargs(
        generation_id=generation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    generation_id: str,
) -> Optional[Union[CharacterGenerationStatus, ErrorMessage]]:
    """Fetches the progress of the generation.

    Args:
        generation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CharacterGenerationStatus, ErrorMessage]
    """

    return sync_detailed(
        client=client,
        generation_id=generation_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    generation_id: str,
) -> Response[Union[CharacterGenerationStatus, ErrorMessage]]:
    """Fetches the progress of the generation.

    Args:
        generation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CharacterGenerationStatus, ErrorMessage]]
    """

    kwargs = _get_kwargs(
        generation_id=generation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    generation_id: str,
) -> Optional[Union[CharacterGenerationStatus, ErrorMessage]]:
    """Fetches the progress of the generation.

    Args:
        generation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CharacterGenerationStatus, ErrorMessage]
    """

    return (
        await asyncio_detailed(
            client=client,
            generation_id=generation_id,
        )
    ).parsed
