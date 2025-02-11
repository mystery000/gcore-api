from unittest.mock import Mock, patch

import pytest

from gcore_api.auth import GcoreAuth
from gcore_api.loadbalancer import LoadBalancerClient


@pytest.fixture
def mock_auth():
    auth = Mock(spec=GcoreAuth)
    auth.get_headers.return_value = {"Authorization": "Bearer test-token"}
    return auth


@pytest.fixture
def lb_client(mock_auth):
    return LoadBalancerClient(mock_auth)


def test_list_load_balancers(lb_client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {
                "id": 1,
                "name": "test-lb",
                "type": "http",
                "status": "active",
                "region": "eu-north-1",
            }
        ]
        lbs = lb_client.list_load_balancers()
        assert len(lbs) == 1
        assert lbs[0]["id"] == 1
        assert lbs[0]["name"] == "test-lb"
        assert lbs[0]["type"] == "http"


def test_create_load_balancer(lb_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "name": "new-lb",
            "type": "http",
            "status": "creating",
            "region": "eu-north-1",
        }
        lb = lb_client.create_load_balancer(name="new-lb", region="eu-north-1")
        assert lb["id"] == 1
        assert lb["name"] == "new-lb"
        assert lb["type"] == "http"


def test_create_listener(lb_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "protocol": "HTTP",
            "port": 80,
        }
        listener = lb_client.create_listener(lb_id=1, protocol="HTTP", port=80)
        assert listener["id"] == 1
        assert listener["protocol"] == "HTTP"
        assert listener["port"] == 80


def test_create_pool(lb_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "protocol": "HTTP",
            "method": "ROUND_ROBIN",
        }
        pool = lb_client.create_pool(lb_id=1, listener_id=1, protocol="HTTP")
        assert pool["id"] == 1
        assert pool["protocol"] == "HTTP"
        assert pool["method"] == "ROUND_ROBIN"


def test_add_member(lb_client):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "id": 1,
            "address": "192.0.2.1",
            "port": 8080,
            "weight": 1,
        }
        member = lb_client.add_member(
            lb_id=1, pool_id=1, address="192.0.2.1", port=8080
        )
        assert member["id"] == 1
        assert member["address"] == "192.0.2.1"
        assert member["port"] == 8080
