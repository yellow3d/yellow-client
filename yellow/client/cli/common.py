import datetime

import click

from yellow.client.types import UNSET

HOST_ENVVAR = "YELLOW_HOST"
HOST_DEFAULT = "https://yellow3d.com"
host_option = click.option(
    "--host",
    default=HOST_DEFAULT,
    envvar=HOST_ENVVAR,
    help=f"Yellow API host. Defaults to {HOST_DEFAULT}. Optionally, set the {HOST_ENVVAR} environment variable.",
)

TOKEN_ENVVAR = "YELLOW_TOKEN"
token_option = click.option(
    "--token",
    prompt=True,
    required=True,
    envvar=TOKEN_ENVVAR,
    help=f"Yellow API token. Use the {TOKEN_ENVVAR} environment variable.",
)

def validate_int(ctx, param, value):
    if value is not None:
        try:
            return int(value)
        except ValueError:
            raise click.BadParameter("Must be an integer")
    return UNSET

def pagination_options(f):
    @click.option("--page-size", help="Page size", required=False, default=None, type=int, callback=validate_int)
    @click.option("--page", help="Page", required=False, default=None, type=int, callback=validate_int)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

def validate_date(ctx, param, value):
    if value is not None:
        try:
            return datetime.datetime.fromisoformat(value).date()
        except ValueError:
            raise click.BadParameter("Date must be in ISO format (YYYY-MM-DD)")
    return UNSET
