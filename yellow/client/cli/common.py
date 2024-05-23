import click

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
