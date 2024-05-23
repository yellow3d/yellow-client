import json
import os
import sys

import click

from yellow.client.api.auth import auth_token_create
from yellow.client.cli.common import host_option
from yellow.client.client import Client
from yellow.client.models.auth_token_request import AuthTokenRequest


@click.command()
@click.option("--username", prompt=True)
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=True
)
@host_option
@click.pass_context
def auth(ctx, host, username, password):
    host = host or ctx.obj.get('HOST')
    request = AuthTokenRequest(username=username, password=password)
    with Client(base_url=host) as client:
        response = auth_token_create.sync_detailed(client=client, body=request)
    if response.parsed is not None:
        print(response.parsed.token)
    elif (errors := json.loads(response.content).get("non_field_errors")) is not None:
        print(*errors, sep="\n", file=sys.stderr)
    return 0 if response.status_code == 200 else 1
