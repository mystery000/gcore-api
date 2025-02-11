#!/usr/bin/env python3
import click
from .auth import GcoreAuth
from .config import Config
from .cdn import CDNClient
from .dns import DNSClient
from .ssl import SSLClient
from .storage import StorageClient

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

@cdn.command()
@click.argument('resource_id', type=int)
@click.argument('urls', nargs=-1, required=True)
@click.pass_context
def purge(ctx, resource_id, urls):
    """Purge specific URLs from CDN cache."""
    try:
        result = ctx.obj['cdn'].purge_url(resource_id, list(urls))
        click.echo("Purge request submitted successfully:")
        click.echo(f"Task ID: {result.get('task_id')}")
        click.echo("Use 'cdn purge-status' command to check the status")
    except Exception as e:
        raise click.ClickException(str(e))

@cdn.command()
@click.argument('resource_id', type=int)
@click.pass_context
def purge_all(ctx, resource_id):
    """Purge all cached content for a resource."""
    try:
        result = ctx.obj['cdn'].purge_all(resource_id)
        click.echo("Purge all request submitted successfully:")
        click.echo(f"Task ID: {result.get('task_id')}")
        click.echo("Use 'cdn purge-status' command to check the status")
    except Exception as e:
        raise click.ClickException(str(e))

@cdn.command()
@click.argument('resource_id', type=int)
@click.argument('task_id')
@click.pass_context
def purge_status(ctx, resource_id, task_id):
    """Get the status of a purge task."""
    try:
        status = ctx.obj['cdn'].get_purge_status(resource_id, task_id)
        click.echo(f"Status: {status.get('status', 'Unknown')}")
        if 'progress' in status:
            click.echo(f"Progress: {status['progress']}%")
        if 'error' in status:
            click.echo(f"Error: {status['error']}")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.group()
@click.pass_context
def dns(ctx):
    """Manage DNS zones and records."""
    token = ctx.obj['config'].load_token()
    if not token:
        raise click.ClickException("No API token configured. Use 'configure' command first.")
    auth = GcoreAuth(token)
    ctx.obj['dns'] = DNSClient(auth)

@dns.group()
def zone():
    """Manage DNS zones."""
    pass

@zone.command('list')
@click.pass_context
def list_zones(ctx):
    """List all DNS zones."""
    try:
        zones = ctx.obj['dns'].list_zones()
        if not zones:
            click.echo("No DNS zones found")
            return
        
        for zone in zones:
            click.echo(f"ID: {zone['id']}")
            click.echo(f"Name: {zone['name']}")
            click.echo(f"Status: {zone.get('status', 'Unknown')}")
            click.echo("---")
    except Exception as e:
        raise click.ClickException(str(e))

@zone.command()
@click.argument('name')
@click.pass_context
def create(ctx, name):
    """Create a new DNS zone."""
    try:
        zone = ctx.obj['dns'].create_zone(name)
        click.echo("DNS zone created successfully:")
        click.echo(f"ID: {zone['id']}")
        click.echo(f"Name: {zone['name']}")
    except Exception as e:
        raise click.ClickException(str(e))

@zone.command()
@click.argument('zone_id', type=int)
@click.pass_context
def delete(ctx, zone_id):
    """Delete a DNS zone."""
    try:
        ctx.obj['dns'].delete_zone(zone_id)
        click.echo("DNS zone deleted successfully")
    except Exception as e:
        raise click.ClickException(str(e))

@dns.group()
def record():
    """Manage DNS records."""
    pass

@record.command('list')
@click.argument('zone_id', type=int)
@click.pass_context
def list_records(ctx, zone_id):
    """List all records in a DNS zone."""
    try:
        records = ctx.obj['dns'].list_records(zone_id)
        if not records:
            click.echo("No DNS records found")
            return
        
        for record in records:
            click.echo(f"ID: {record['id']}")
            click.echo(f"Name: {record['name']}")
            click.echo(f"Type: {record['type']}")
            click.echo(f"Content: {record['content']}")
            click.echo(f"TTL: {record.get('ttl', 3600)}")
            click.echo("---")
    except Exception as e:
        raise click.ClickException(str(e))

@record.command()
@click.argument('zone_id', type=int)
@click.argument('name')
@click.argument('type')
@click.argument('content')
@click.option('--ttl', type=int, default=3600, help='Time to live in seconds')
@click.pass_context
def create(ctx, zone_id, name, type, content, ttl):
    """Create a new DNS record."""
    try:
        record = ctx.obj['dns'].create_record(
            zone_id=zone_id,
            name=name,
            type=type,
            content=content,
            ttl=ttl
        )
        click.echo("DNS record created successfully:")
        click.echo(f"ID: {record['id']}")
        click.echo(f"Name: {record['name']}")
        click.echo(f"Type: {record['type']}")
        click.echo(f"Content: {record['content']}")
        click.echo(f"TTL: {record.get('ttl', 3600)}")
    except Exception as e:
        raise click.ClickException(str(e))

@record.command()
@click.argument('zone_id', type=int)
@click.argument('record_id', type=int)
@click.pass_context
def delete(ctx, zone_id, record_id):
    """Delete a DNS record."""
    try:
        ctx.obj['dns'].delete_record(zone_id, record_id)
        click.echo("DNS record deleted successfully")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.group()
@click.pass_context
def ssl(ctx):
    """Manage SSL certificates."""
    token = ctx.obj['config'].load_token()
    if not token:
        raise click.ClickException("No API token configured. Use 'configure' command first.")
    auth = GcoreAuth(token)
    ctx.obj['ssl'] = SSLClient(auth)

@ssl.command('list')
@click.pass_context
def list_certificates(ctx):
    """List all SSL certificates."""
    try:
        certs = ctx.obj['ssl'].list_certificates()
        if not certs:
            click.echo("No SSL certificates found")
            return
        
        for cert in certs:
            click.echo(f"ID: {cert['id']}")
            click.echo(f"Name: {cert['name']}")
            click.echo(f"Status: {cert.get('status', 'Unknown')}")
            click.echo(f"Expires: {cert.get('expires_at', 'Unknown')}")
            click.echo("Domains:")
            for domain in cert.get('domains', []):
                click.echo(f"  - {domain}")
            click.echo("---")
    except Exception as e:
        raise click.ClickException(str(e))

@ssl.command()
@click.argument('cert_id', type=int)
@click.pass_context
def get(ctx, cert_id):
    """Get details of a specific SSL certificate."""
    try:
        cert = ctx.obj['ssl'].get_certificate(cert_id)
        click.echo(f"ID: {cert['id']}")
        click.echo(f"Name: {cert['name']}")
        click.echo(f"Status: {cert.get('status', 'Unknown')}")
        click.echo(f"Expires: {cert.get('expires_at', 'Unknown')}")
        click.echo("Domains:")
        for domain in cert.get('domains', []):
            click.echo(f"  - {domain}")
    except Exception as e:
        raise click.ClickException(str(e))

@ssl.command()
@click.argument('name')
@click.argument('cert_file', type=click.Path(exists=True))
@click.argument('key_file', type=click.Path(exists=True))
@click.option('--chain-file', type=click.Path(exists=True), help='Certificate chain file')
@click.pass_context
def upload(ctx, name, cert_file, key_file, chain_file):
    """Upload a custom SSL certificate."""
    try:
        with open(cert_file) as f:
            cert = f.read()
        with open(key_file) as f:
            key = f.read()
        chain = None
        if chain_file:
            with open(chain_file) as f:
                chain = f.read()
                
        cert = ctx.obj['ssl'].upload_certificate(
            name=name,
            cert=cert,
            private_key=key,
            chain=chain
        )
        click.echo("SSL certificate uploaded successfully:")
        click.echo(f"ID: {cert['id']}")
        click.echo(f"Name: {cert['name']}")
        click.echo(f"Status: {cert.get('status', 'Unknown')}")
    except Exception as e:
        raise click.ClickException(str(e))

@ssl.command()
@click.argument('domains', nargs=-1, required=True)
@click.option('--validation-method', type=click.Choice(['dns', 'http']), default='dns',
              help='Domain validation method')
@click.pass_context
def request(ctx, domains, validation_method):
    """Request a new SSL certificate through Gcore."""
    try:
        cert = ctx.obj['ssl'].request_certificate(
            domains=list(domains),
            validation_method=validation_method
        )
        click.echo("SSL certificate requested successfully:")
        click.echo(f"ID: {cert['id']}")
        click.echo(f"Status: {cert.get('status', 'Unknown')}")
        click.echo("Validation required for domains:")
        for domain in cert.get('domains', []):
            click.echo(f"  - {domain}")
        click.echo("\nUse 'ssl validation-status' command to check validation status")
    except Exception as e:
        raise click.ClickException(str(e))

@ssl.command()
@click.argument('cert_id', type=int)
@click.pass_context
def validation_status(ctx, cert_id):
    """Get domain validation status for a certificate request."""
    try:
        status = ctx.obj['ssl'].get_validation_status(cert_id)
        click.echo(f"Certificate ID: {cert_id}")
        click.echo(f"Overall Status: {status.get('status', 'Unknown')}")
        click.echo("\nDomain Validation Status:")
        for domain in status.get('domains', []):
            click.echo(f"\nDomain: {domain.get('name')}")
            click.echo(f"Status: {domain.get('status', 'Unknown')}")
            if domain.get('validation_records'):
                click.echo("Validation Records:")
                for record in domain['validation_records']:
                    click.echo(f"  Type: {record.get('type')}")
                    click.echo(f"  Name: {record.get('name')}")
                    click.echo(f"  Value: {record.get('value')}")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.group()
@click.pass_context
def storage(ctx):
    """Manage storage buckets and objects."""
    token = ctx.obj['config'].load_token()
    if not token:
        raise click.ClickException("No API token configured. Use 'configure' command first.")
    auth = GcoreAuth(token)
    ctx.obj['storage'] = StorageClient(auth)

@storage.group()
def bucket():
    """Manage storage buckets."""
    pass

@bucket.command('list')
@click.pass_context
def list_buckets(ctx):
    """List all storage buckets."""
    try:
        buckets = ctx.obj['storage'].list_buckets()
        if not buckets:
            click.echo("No storage buckets found")
            return
        
        for bucket in buckets:
            click.echo(f"Name: {bucket['name']}")
            click.echo(f"Location: {bucket.get('location', 'Unknown')}")
            click.echo(f"Access: {bucket.get('access', 'private')}")
            click.echo("---")
    except Exception as e:
        raise click.ClickException(str(e))

@bucket.command()
@click.argument('name')
@click.option('--location', default='eu-north-1', help='Bucket location')
@click.option('--access', type=click.Choice(['private', 'public-read']), 
              default='private', help='Bucket access level')
@click.pass_context
def create(ctx, name, location, access):
    """Create a new storage bucket."""
    try:
        bucket = ctx.obj['storage'].create_bucket(
            name=name,
            location=location,
            access=access
        )
        click.echo("Storage bucket created successfully:")
        click.echo(f"Name: {bucket['name']}")
        click.echo(f"Location: {bucket.get('location')}")
        click.echo(f"Access: {bucket.get('access')}")
    except Exception as e:
        raise click.ClickException(str(e))

@bucket.command()
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """Delete a storage bucket."""
    try:
        ctx.obj['storage'].delete_bucket(name)
        click.echo("Storage bucket deleted successfully")
    except Exception as e:
        raise click.ClickException(str(e))

@storage.group()
def object():
    """Manage storage objects."""
    pass

@object.command('list')
@click.argument('bucket')
@click.option('--prefix', help='Filter objects by prefix')
@click.option('--delimiter', help='Delimiter for hierarchy')
@click.pass_context
def list_objects(ctx, bucket, prefix, delimiter):
    """List objects in a bucket."""
    try:
        result = ctx.obj['storage'].list_objects(
            bucket_name=bucket,
            prefix=prefix,
            delimiter=delimiter
        )
        
        if not result.get('objects'):
            click.echo("No objects found")
            return
            
        for obj in result['objects']:
            click.echo(f"Name: {obj['name']}")
            click.echo(f"Size: {obj.get('size', 0)} bytes")
            click.echo(f"Last Modified: {obj.get('last_modified', 'Unknown')}")
            click.echo("---")
    except Exception as e:
        raise click.ClickException(str(e))

@object.command()
@click.argument('bucket')
@click.argument('object_name')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--content-type', help='Content type of the object')
@click.pass_context
def upload(ctx, bucket, object_name, file_path, content_type):
    """Upload an object to a bucket."""
    try:
        result = ctx.obj['storage'].upload_object(
            bucket_name=bucket,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type
        )
        click.echo("Object uploaded successfully:")
        click.echo(f"Bucket: {bucket}")
        click.echo(f"Object: {object_name}")
        click.echo(f"Size: {result.get('size', 0)} bytes")
    except Exception as e:
        raise click.ClickException(str(e))

@object.command()
@click.argument('bucket')
@click.argument('object_name')
@click.option('--output', type=click.Path(), help='Output file path')
@click.pass_context
def download(ctx, bucket, object_name, output):
    """Download an object from a bucket."""
    try:
        ctx.obj['storage'].download_object(
            bucket_name=bucket,
            object_name=object_name,
            file_path=output
        )
        click.echo("Object downloaded successfully")
    except Exception as e:
        raise click.ClickException(str(e))

@object.command()
@click.argument('bucket')
@click.argument('object_name')
@click.pass_context
def delete(ctx, bucket, object_name):
    """Delete an object from a bucket."""
    try:
        ctx.obj['storage'].delete_object(bucket, object_name)
        click.echo("Object deleted successfully")
    except Exception as e:
        raise click.ClickException(str(e))

def main():
    """Entry point for the CLI."""
    cli(obj={})

if __name__ == "__main__":
    main()
