from unittest.mock import Mock, patch

import pytest

from gcore_api.auth import GcoreAuth
from gcore_api.storage import StorageClient


@pytest.fixture
def mock_auth():
    auth = Mock(spec=GcoreAuth)
    auth.get_headers.return_value = {"Authorization": "Bearer test-token"}
    return auth


@pytest.fixture
def storage_client(mock_auth):
    return StorageClient(mock_auth)


def test_list_buckets(storage_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"name": "test-bucket", "location": "eu-north-1", "access": "private"}
        ]
        buckets = storage_client.list_buckets()
        assert len(buckets) == 1
        assert buckets[0]["name"] == "test-bucket"
        assert buckets[0]["location"] == "eu-north-1"


def test_create_bucket(storage_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "name": "new-bucket",
            "location": "eu-north-1",
            "access": "private",
        }
        bucket = storage_client.create_bucket("new-bucket")
        assert bucket["name"] == "new-bucket"
        assert bucket["location"] == "eu-north-1"


def test_list_objects(storage_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "objects": [
                {
                    "name": "test.txt",
                    "size": 1024,
                    "last_modified": "2024-02-11T12:00:00Z",
                }
            ]
        }
        result = storage_client.list_objects("test-bucket")
        assert len(result["objects"]) == 1
        assert result["objects"][0]["name"] == "test.txt"
        assert result["objects"][0]["size"] == 1024


@patch("builtins.open")
def test_upload_object(mock_open, storage_client):
    with patch("requests.put") as mock_put:
        mock_put.return_value.json.return_value = {"name": "test.txt", "size": 1024}
        result = storage_client.upload_object(
            "test-bucket", "test.txt", "local/test.txt"
        )
        assert result["name"] == "test.txt"
        assert result["size"] == 1024
