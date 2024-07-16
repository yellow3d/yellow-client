from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.character_feedback import CharacterFeedback
from ...models.character_feedback_request import CharacterFeedbackRequest
from ...models.error_message import ErrorMessage
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
    ],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/sculpt/characters/feedback",
    }

    if isinstance(body, CharacterFeedbackRequest):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, CharacterFeedbackRequest):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, CharacterFeedbackRequest):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CharacterFeedback, ErrorMessage]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CharacterFeedback.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CharacterFeedback, ErrorMessage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
    ],
) -> Response[Union[CharacterFeedback, ErrorMessage]]:
    """Submits a feedback for a character.

    Args:
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CharacterFeedback, ErrorMessage]]
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
    body: Union[
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
    ],
) -> Optional[Union[CharacterFeedback, ErrorMessage]]:
    """Submits a feedback for a character.

    Args:
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CharacterFeedback, ErrorMessage]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
    ],
) -> Response[Union[CharacterFeedback, ErrorMessage]]:
    """Submits a feedback for a character.

    Args:
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CharacterFeedback, ErrorMessage]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
        CharacterFeedbackRequest,
    ],
) -> Optional[Union[CharacterFeedback, ErrorMessage]]:
    """Submits a feedback for a character.

    Args:
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):
        body (CharacterFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CharacterFeedback, ErrorMessage]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
