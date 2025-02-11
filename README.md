# Gcore API CLI Tool

A command-line interface for interacting with the Gcore API.

## Installation

```bash
pip install gcore-api
```

## Authentication

Before using the tool, you need to get an API token from Gcore:

1. Log in to your Gcore Control Panel at https://auth.gcore.com/login
2. Go to API section
3. Generate a new permanent token
4. Use this token to configure the CLI

Configure the CLI with your token:

```bash
gcore configure YOUR_API_TOKEN
```

You can also set the token via environment variable:

```bash
export GCORE_API_TOKEN=YOUR_API_TOKEN
```

## Usage

### Authentication Commands

Verify your authentication:
```bash
gcore verify
```

### CDN Commands

List all CDN resources:
```bash
gcore cdn list
```

Get details of a specific CDN resource:
```bash
gcore cdn get RESOURCE_ID
```

Create a new CDN resource:
```bash
gcore cdn create ORIGIN [--cname CNAME] [--ssl/--no-ssl]
```

Example:
```bash
gcore cdn create example.com --cname cdn.example.com --ssl
```

Purge specific URLs from cache:
```bash
gcore cdn purge RESOURCE_ID URL [URL...]
```

Example:
```bash
gcore cdn purge 123 https://cdn.example.com/image.jpg https://cdn.example.com/style.css
```

Purge all cached content:
```bash
gcore cdn purge-all RESOURCE_ID
```

Check purge task status:
```bash
gcore cdn purge-status RESOURCE_ID TASK_ID
```

### DNS Commands

List all DNS zones:
```bash
gcore dns zone list
```

Create a new DNS zone:
```bash
gcore dns zone create ZONE_NAME
```

Delete a DNS zone:
```bash
gcore dns zone delete ZONE_ID
```

List records in a DNS zone:
```bash
gcore dns record list ZONE_ID
```

Create a new DNS record:
```bash
gcore dns record create ZONE_ID NAME TYPE CONTENT [--ttl TTL]
```

Example:
```bash
gcore dns record create 123 www A 192.0.2.1 --ttl 3600
```

Delete a DNS record:
```bash
gcore dns record delete ZONE_ID RECORD_ID
```

### SSL Certificate Commands

List all SSL certificates:
```bash
gcore ssl list
```

Get certificate details:
```bash
gcore ssl get CERT_ID
```

Upload a custom certificate:
```bash
gcore ssl upload NAME CERT_FILE KEY_FILE [--chain-file CHAIN_FILE]
```

Request a new certificate:
```bash
gcore ssl request DOMAIN [DOMAIN...] [--validation-method dns|http]
```

Check validation status:
```bash
gcore ssl validation-status CERT_ID
```

## Development

This project uses Poetry for dependency management. To set up the development environment:

1. Install Poetry
2. Clone the repository
3. Run `poetry install`
4. Run `poetry shell` to activate the virtual environment

## Testing

Run tests using pytest:

```bash
poetry run pytest
```

## Error Handling

Common errors and solutions:

- "No API token configured": Run `gcore configure YOUR_API_TOKEN` with a valid token
- "Invalid API token": Make sure your token is valid and not expired
- "API request failed": Check your internet connection and Gcore API status
