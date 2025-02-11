# Gcore API CLI Tool

[![CI/CD](https://github.com/mystery000/gcore-api/actions/workflows/ci.yml/badge.svg)](https://github.com/mystery000/gcore-api/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/gcore-api.svg)](https://badge.fury.io/py/gcore-api)
[![Python versions](https://img.shields.io/pypi/pyversions/gcore-api.svg)](https://pypi.org/project/gcore-api/)

A comprehensive command-line interface for interacting with Gcore's API services.

## Features

- CDN resource management
- DNS zones and records management
- SSL certificate management
- Storage buckets and objects management
- Load balancer management

## Installation

```bash
pip install gcore-api
```

## Quick Start

1. Get your API token from Gcore Control Panel
2. Configure the CLI:
```bash
gcore configure YOUR_API_TOKEN
```

## Usage

### CDN Management

```bash
# List CDN resources
gcore cdn list

# Create CDN resource
gcore cdn create example.com --cname cdn.example.com

# Purge cache
gcore cdn purge RESOURCE_ID https://example.com/image.jpg
```

### DNS Management

```bash
# List DNS zones
gcore dns zone list

# Create zone
gcore dns zone create example.com

# Add record
gcore dns record create ZONE_ID www A 192.0.2.1
```

### SSL Certificates

```bash
# List certificates
gcore ssl list

# Request certificate
gcore ssl request example.com www.example.com

# Check validation status
gcore ssl validation-status CERT_ID
```

### Storage Management

```bash
# List buckets
gcore storage bucket list

# Create bucket
gcore storage bucket create my-bucket

# Upload file
gcore storage object upload my-bucket file.txt /path/to/file.txt
```

## Development

1. Clone the repository
2. Install dependencies:
```bash
poetry install
```

3. Run tests:
```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
