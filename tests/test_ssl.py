import pytest
from unittest.mock import Mock, patch
from gcore_api.ssl import SSLClient
from gcore_api.auth import GcoreAuth

@pytest.fixture
def mock_auth():
    auth = Mock(spec=GcoreAuth)
    auth.get_headers.return_value = {"Authorization": "Bearer test-token"}
    return auth

@pytest.fixture
def ssl_client(mock_auth):
    return SSLClient(mock_auth)

def test_list_certificates(ssl_client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = [
            {
                "id": 1,
                "name": "example.com",
                "status": "active",
                "domains": ["example.com", "www.example.com"]
            }
        ]
        certs = ssl_client.list_certificates()
        assert len(certs) == 1
        assert certs[0]["id"] == 1
        assert certs[0]["name"] == "example.com"
        assert len(certs[0]["domains"]) == 2

def test_upload_certificate(ssl_client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "name": "custom-cert",
            "status": "active"
        }
        cert = ssl_client.upload_certificate(
            name="custom-cert",
            cert="CERT_CONTENT",
            private_key="KEY_CONTENT"
        )
        assert cert["id"] == 1
        assert cert["name"] == "custom-cert"
        assert cert["status"] == "active"

def test_request_certificate(ssl_client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "status": "pending_validation",
            "domains": ["example.com"]
        }
        cert = ssl_client.request_certificate(
            domains=["example.com"],
            validation_method="dns"
        )
        assert cert["id"] == 1
        assert cert["status"] == "pending_validation"
        assert "example.com" in cert["domains"]

def test_get_validation_status(ssl_client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "status": "pending",
            "domains": [
                {
                    "name": "example.com",
                    "status": "pending",
                    "validation_records": [
                        {
                            "type": "CNAME",
                            "name": "_validation.example.com",
                            "value": "validation.gcore.com"
                        }
                    ]
                }
            ]
        }
        status = ssl_client.get_validation_status(1)
        assert status["status"] == "pending"
        assert len(status["domains"]) == 1
        assert status["domains"][0]["name"] == "example.com"
