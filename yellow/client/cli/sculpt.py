from datetime import datetime
import re
import uuid
from pathlib import Path

import click

from yellow.client import models
from yellow.client.api.sculpt import (sculpt_characters_create,
                                      sculpt_characters_fetch_retrieve,
                                      sculpt_characters_list,
                                      sculpt_characters_status_retrieve, sculpt_characters_cancel_partial_update, sculpt_characters_feedback_create)
from yellow.client.cli.common import host_option, token_option, pagination_options, validate_date
from yellow.client.client import AuthenticatedClient

FILENAME_PATTERN = re.compile(r'attachment; filename="([^"]+)"')

@click.group()
@host_option
@click.pass_context
def sculpt(ctx, host):
    ctx.obj['HOST'] = host or ctx.obj.get('HOST')

@sculpt.command()
@click.option("--prompt", required=True, prompt=True, help="The prompt for the character.")
@click.option(
    "--gender", required=True, prompt=True, type=models.GenderEnum, help=f"One of: [{', '.join(models.GenderEnum)}]"
)
@token_option
@host_option
@click.pass_context
def create(ctx, host, token, prompt, gender):
    host = host or ctx.obj.get('HOST')
    request = models.CharacterSpecRequest(prompt, gender)
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = sculpt_characters_create.sync_detailed(client=client, body=request)
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@sculpt.command(name="list")
@click.option(
    "--start-date",
    required=False,
    default=None,
    callback=validate_date,
    help="Start of interval for generation date.",
)
@click.option(
    "--end-date",
    required=False,
    default=None,
    callback=validate_date,
    help="End of interval for generation date.",
)
@click.option(
    "--state",
    multiple=True,
    type=models.SculptCharactersListStateItem,
    help=f"One of: [{', '.join(models.SculptCharactersListStateItem)}]",
)
@token_option
@host_option
@pagination_options
@click.pass_context
def list(ctx, host, token, **kwargs):
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        kwargs["client"] = client
        response = sculpt_characters_list.sync_detailed(**kwargs)
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@sculpt.command(help=f"Cancel generation with given UUID")
@click.argument("generation_id", type=uuid.UUID)
@token_option
@host_option
@click.pass_context
def cancel(ctx, host, token, generation_id):
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = sculpt_characters_cancel_partial_update.sync_detailed(
            client=client, generation_id=generation_id,
        )
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

sculpt_characters_feedback_create

@sculpt.command(help=f"Submits a feedback for a character with given UUID")
@click.argument("generation_id", type=uuid.UUID)
@click.argument("feedback", type=str)
@token_option
@host_option
@click.pass_context
def feedback(ctx, host, token, generation_id, feedback):
    host = host or ctx.obj.get('HOST')
    request = models.CharacterFeedbackRequest(feedback, str(generation_id))
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = sculpt_characters_feedback_create.sync_detailed(
            client=client, body=request,
        )
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@sculpt.command(help=f"Fetches status of generation with given UUID")
@click.argument("generation_id", type=uuid.UUID)
@token_option
@host_option
@click.pass_context
def status(ctx, host, token, generation_id):
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = sculpt_characters_status_retrieve.sync_detailed(
            client=client, generation_id=generation_id,
        )
    print(response.content.decode())
    return 0 if response.status_code == 200 else 1

@sculpt.command(help=f"Fetches generated model with given UUID")
@click.argument("generation_id", type=uuid.UUID)
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
def fetch(ctx, host, token, generation_id, output: Path, overwrite: bool):
    if not overwrite and output.is_file():
        click.confirm(f"Overwrite {output}?", abort=True)
    host = host or ctx.obj.get('HOST')
    with AuthenticatedClient(base_url=host, token=token) as client:
        response = sculpt_characters_fetch_retrieve.sync_detailed(
            client=client, generation_id=generation_id,
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
