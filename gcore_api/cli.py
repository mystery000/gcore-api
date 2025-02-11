#!/usr/bin/env python3
import click
from .auth import GcoreAuth
from .config import Config
from .cdn import CDNClient

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

@cli.group()
@click.pass_context
def cdn(ctx):
    """Manage CDN resources."""
    token = ctx.obj['config'].load_token()
    if not token:
        raise click.ClickException("No API token configured. Use 'configure' command first.")
    auth = GcoreAuth(token)
    ctx.obj['cdn'] = CDNClient(auth)

@cdn.command()
@click.pass_context
def list(ctx):
    """List all CDN resources."""
    try:
        resources = ctx.obj['cdn'].list_resources()
        if not resources:
            click.echo("No CDN resources found")
            return
        
        for resource in resources:
            click.echo(f"ID: {resource['id']}")
            click.echo(f"Origin: {resource['origin']}")
            click.echo(f"CNAME: {resource.get('cname', 'Not set')}")
            click.echo(f"SSL: {'Enabled' if resource.get('ssl') else 'Disabled'}")
            click.echo("---")
    except Exception as e:
        raise click.ClickException(str(e))

@cdn.command()
@click.argument('resource_id', type=int)
@click.pass_context
def get(ctx, resource_id):
    """Get details of a specific CDN resource."""
    try:
        resource = ctx.obj['cdn'].get_resource(resource_id)
        click.echo(f"ID: {resource['id']}")
        click.echo(f"Origin: {resource['origin']}")
        click.echo(f"CNAME: {resource.get('cname', 'Not set')}")
        click.echo(f"SSL: {'Enabled' if resource.get('ssl') else 'Disabled'}")
        click.echo(f"Status: {resource.get('status', 'Unknown')}")
    except Exception as e:
        raise click.ClickException(str(e))

@cdn.command()
@click.argument('origin')
@click.option('--cname', help='Custom CNAME for the resource')
@click.option('--ssl/--no-ssl', default=True, help='Enable or disable SSL')
@click.pass_context
def create(ctx, origin, cname, ssl):
    """Create a new CDN resource."""
    try:
        resource = ctx.obj['cdn'].create_resource(origin=origin, cname=cname, ssl=ssl)
        click.echo("CDN resource created successfully:")
        click.echo(f"ID: {resource['id']}")
        click.echo(f"Origin: {resource['origin']}")
        click.echo(f"CNAME: {resource.get('cname', 'Not set')}")
        click.echo(f"SSL: {'Enabled' if resource.get('ssl') else 'Disabled'}")
    except Exception as e:
        raise click.ClickException(str(e))

def main():
    """Entry point for the CLI."""
    cli(obj={})

if __name__ == "__main__":
    main()
