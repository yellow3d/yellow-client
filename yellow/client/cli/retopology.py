import re
import uuid
from pathlib import Path

import click

from yellow.client import models, types
from yellow.client.api.retopology import (
    retopology_characters_create_create, retopology_characters_fetch_retrieve,
    retopology_characters_list, retopology_characters_status_retrieve)
from yellow.client.cli.common import host_option, token_option
from yellow.client.client import AuthenticatedClient

FILENAME_PATTERN = re.compile(r'attachment; filename="([^"]+)"')

@click.group()
@host_option
@click.pass_context
def retopology(ctx, host):
    ctx.obj['HOST'] = host or ctx.obj.get('HOST')

@retopology.command()
@click.argument("file", type=click.File("rb"))
@click.option(
    "--gender", required=False, type=models.GenderEnum, help=f"One of: [{', '.join(models.GenderEnum)}]"
)
@click.option(
    "--genesis", required=False, type=models.GenesisEnum, help=f"One of: [{', '.join(models.GenesisEnum)}]"
)
@token_option
@host_option
@click.pass_context
def create(ctx, host, token, file, gender, genesis):
    host = host or ctx.obj.get('HOST')
    kwargs = {
        "file": types.File(
            payload=file.read(),
            file_name=Path(file.name).name,
            mime_type="model",
        )
    }
    if gender:
        kwargs["gender"] = gender
    if genesis:
        kwargs["genesis"] = genesis
    request = models.FileUploadRequest(**kwargs)
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = retopology_characters_create_create.sync_detailed(client=client, body=request)
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@retopology.command()
@click.option(
    "--state",
    multiple=True,
    type=models.RetopologyCharactersListStateItem,
    help=f"One of: [{', '.join(models.RetopologyCharactersListStateItem)}]",
)
@token_option
@host_option
@click.pass_context
def list(ctx, host, token, state):
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        kwargs = {"client": client}
        if state:
            kwargs["state"] = state
        response = retopology_characters_list.sync_detailed(**kwargs)
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@retopology.command(help=f"Fetches the progress of retopology process with given UUID")
@click.argument("retopology_id", type=uuid.UUID)
@token_option
@host_option
@click.pass_context
def status(ctx, host, token, retopology_id):
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = retopology_characters_status_retrieve.sync_detailed(
            client=client, retopology_id=retopology_id,
        )
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@retopology.command(help=f"Fetches the character with new topology with given UUID")
@click.argument("retopology_id", type=uuid.UUID)
@click.option(
    "-o", "--output", type=Path, default=Path(),
    help="Output file.",
)
@click.option(
    "--overwrite", is_flag=False, default=False,
    help="Confirm overwriting output file if already exists.",
)
@token_option
@host_option
@click.pass_context
def fetch(ctx, host, token, retopology_id, output: Path, overwrite: bool):
    if not overwrite and output.is_file():
        click.confirm(f"Overwrite {output}?", abort=True)
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = retopology_characters_fetch_retrieve.sync_detailed(
            client=client, retopology_id=retopology_id,
        )
    if response.status_code == 200:
        if match := FILENAME_PATTERN.match(response.headers["content-disposition"]):
            filename = match.group(1)
        if output.is_dir():
            output /= filename
            if not overwrite and output.is_file():
                click.confirm(f"Overwrite {output}?", abort=True)
        with output.open("wb") as f:
            f.write(response.content)
    else:
        print(response.content.decode())
    return 0 if response.status_code == 200 else 1
