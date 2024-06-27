from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sculpt_characters_fetch_retrieve_file_format import SculptCharactersFetchRetrieveFileFormat
from ...models.sculpt_characters_fetch_retrieve_rig_type import SculptCharactersFetchRetrieveRigType
from ...types import UNSET, Response
from ...models.file_format_enum import FileFormatEnum
from ...models.rig_type_enum import RigTypeEnum


def _get_kwargs(
    *,
    file_format: SculptCharactersFetchRetrieveFileFormat,
    generation_id: str,
    rig_type: SculptCharactersFetchRetrieveRigType,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_file_format = file_format.value
    params["file_format"] = json_file_format

    params["generation_id"] = generation_id
    params["file_format"] = file_format
    params["rig_type"] = rig_type

    json_rig_type = rig_type.value
    params["rig_type"] = json_rig_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/sculpt/characters/fetch",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    file_format: SculptCharactersFetchRetrieveFileFormat,
    generation_id: str,
    rig_type: SculptCharactersFetchRetrieveRigType,
) -> Response[Any]:
    """Fetches the generated character.

    Args:
        file_format (SculptCharactersFetchRetrieveFileFormat):
        generation_id (str):
        rig_type (SculptCharactersFetchRetrieveRigType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        file_format=file_format,
        generation_id=generation_id,
        rig_type=rig_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    file_format: SculptCharactersFetchRetrieveFileFormat,
    generation_id: str,
    rig_type: SculptCharactersFetchRetrieveRigType,
) -> Response[Any]:
    """Fetches the generated character.

    Args:
        file_format (SculptCharactersFetchRetrieveFileFormat):
        generation_id (str):
        rig_type (SculptCharactersFetchRetrieveRigType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        file_format=file_format,
        generation_id=generation_id,
        rig_type=rig_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
