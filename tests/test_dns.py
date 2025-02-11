from unittest.mock import Mock, patch

import pytest

from gcore_api.auth import GcoreAuth
from gcore_api.dns import DNSClient


@pytest.fixture
def mock_auth():
    auth = Mock(spec=GcoreAuth)
    auth.get_headers.return_value = {"Authorization": "Bearer test-token"}
    return auth


@pytest.fixture
def dns_client(mock_auth):
    return DNSClient(mock_auth)


def test_list_zones(dns_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "example.com", "status": "active"}
        ]
        zones = dns_client.list_zones()
        assert len(zones) == 1
        assert zones[0]["id"] == 1
        assert zones[0]["name"] == "example.com"


def test_create_zone(dns_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "name": "example.com",
            "status": "active",
        }
        zone = dns_client.create_zone("example.com")
        assert zone["id"] == 1
        assert zone["name"] == "example.com"


def test_list_records(dns_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "www", "type": "A", "content": "192.0.2.1", "ttl": 3600}
        ]
        records = dns_client.list_records(1)
        assert len(records) == 1
        assert records[0]["id"] == 1
        assert records[0]["type"] == "A"
        assert records[0]["content"] == "192.0.2.1"


def test_create_record(dns_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "name": "www",
            "type": "A",
            "content": "192.0.2.1",
            "ttl": 3600,
        }
        record = dns_client.create_record(
            zone_id=1, name="www", type="A", content="192.0.2.1", ttl=3600
        )
        assert record["id"] == 1
        assert record["name"] == "www"
        assert record["type"] == "A"
        assert record["content"] == "192.0.2.1"
