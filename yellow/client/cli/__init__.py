import click

# from .client import AuthenticatedClient, Client
from yellow.client.cli.auth import auth
from yellow.client.cli.common import host_option
from yellow.client.cli.sculpt import sculpt


@click.group()
@host_option
@click.pass_context
def cli(ctx, host):
    ctx.ensure_object(dict)
    ctx.obj['HOST'] = host

cli.add_command(auth)
cli.add_command(sculpt)

if __name__ == "__main__":
    cli()
