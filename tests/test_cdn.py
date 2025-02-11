from unittest.mock import Mock, patch

import pytest

from gcore_api.auth import GcoreAuth
from gcore_api.cdn import CDNClient


@pytest.fixture
def mock_auth():
    auth = Mock(spec=GcoreAuth)
    auth.get_headers.return_value = {"Authorization": "Bearer test-token"}
    return auth


@pytest.fixture
def cdn_client(mock_auth):
    return CDNClient(mock_auth)


def test_list_resources(cdn_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"id": 1, "origin": "example.com", "ssl": True}
        ]
        resources = cdn_client.list_resources()
        assert len(resources) == 1
        assert resources[0]["id"] == 1
        assert resources[0]["origin"] == "example.com"


def test_get_resource(cdn_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "id": 1,
            "origin": "example.com",
            "ssl": True,
        }
        resource = cdn_client.get_resource(1)
        assert resource["id"] == 1
        assert resource["origin"] == "example.com"


def test_create_resource(cdn_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "origin": "example.com",
            "cname": "cdn.example.com",
            "ssl": True,
        }
        resource = cdn_client.create_resource(
            origin="example.com", cname="cdn.example.com", ssl=True
        )
        assert resource["id"] == 1
        assert resource["origin"] == "example.com"
        assert resource["cname"] == "cdn.example.com"


def test_purge_url(cdn_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "task_id": "task-123",
            "status": "pending",
        }
        result = cdn_client.purge_url(1, ["https://example.com/image.jpg"])
        assert result["task_id"] == "task-123"
        assert result["status"] == "pending"


def test_purge_all(cdn_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "task_id": "task-123",
            "status": "pending",
        }
        result = cdn_client.purge_all(1)
        assert result["task_id"] == "task-123"
        assert result["status"] == "pending"


def test_get_purge_status(cdn_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "task_id": "task-123",
            "status": "completed",
            "progress": 100,
        }
        status = cdn_client.get_purge_status(1, "task-123")
        assert status["status"] == "completed"
        assert status["progress"] == 100
