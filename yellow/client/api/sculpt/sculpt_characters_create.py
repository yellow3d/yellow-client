from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.character_spec_request import CharacterSpecRequest
from ...models.error_message import ErrorMessage
from ...models.uuid import UUID
from ...types import Response


def _get_kwargs(
    *,
    body: CharacterSpecRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/sculpt/characters",
    }

    _json_body = body.to_dict()

    _kwargs["json"] = _json_body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorMessage, UUID]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.CREATED:
        response_201 = UUID.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorMessage, UUID]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CharacterSpecRequest,
) -> Response[Union[ErrorMessage, UUID]]:
    """Launches generation of a new character.

    Args:
        body (CharacterSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, UUID]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CharacterSpecRequest,
) -> Optional[Union[ErrorMessage, UUID]]:
    """Launches generation of a new character.

    Args:
        body (CharacterSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, UUID]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CharacterSpecRequest,
) -> Response[Union[ErrorMessage, UUID]]:
    """Launches generation of a new character.

    Args:
        body (CharacterSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, UUID]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CharacterSpecRequest,
) -> Optional[Union[ErrorMessage, UUID]]:
    """Launches generation of a new character.

    Args:
        body (CharacterSpecRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, UUID]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
