#!/usr/bin/env python3
import click
from .auth import GcoreAuth
from .config import Config

@click.group()
@click.pass_context
def cli(ctx):
    """Gcore API command-line tool."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config()

@cli.command()
@click.argument('token')
@click.pass_context
def configure(ctx, token):
    """Configure Gcore CLI with API token."""
    try:
        # Validate token before saving
        auth = GcoreAuth(token)
        if not auth.validate_token():
            raise click.ClickException("Invalid API token")
        
        # Save valid token
        ctx.obj['config'].save_token(token)
        click.echo("Configuration saved successfully")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.pass_context
def verify(ctx):
    """Verify authentication token."""
    token = ctx.obj['config'].load_token()
    if not token:
        raise click.ClickException("No API token configured. Use 'configure' command first.")
    
    try:
        auth = GcoreAuth(token)
        if auth.validate_token():
            click.echo("Token is valid")
        else:
            click.echo("Token is invalid")
    except Exception as e:
        raise click.ClickException(str(e))

def main():
    """Entry point for the CLI."""
    cli(obj={})

if __name__ == "__main__":
    main()
