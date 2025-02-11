import requests
from typing import List, Dict, Optional

class LoadBalancerClient:
    """Client for Gcore Load Balancer API operations."""
    
    BASE_URL = "https://api.gcore.com/loadbalancer/v1"
    
    def __init__(self, auth):
        self.auth = auth
    
    def list_load_balancers(self) -> List[Dict]:
        """List all load balancers."""
        response = requests.get(
            f"{self.BASE_URL}/loadbalancers",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_load_balancer(self, lb_id: int) -> Dict:
        """Get details of a specific load balancer."""
        response = requests.get(
            f"{self.BASE_URL}/loadbalancers/{lb_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_load_balancer(self,
                           name: str,
                           region: str,
                           type: str = "http",
                           flavor: str = "lb1-1-1") -> Dict:
        """Create a new load balancer."""
        data = {
            "name": name,
            "region": region,
            "type": type,
            "flavor": flavor
        }
        response = requests.post(
            f"{self.BASE_URL}/loadbalancers",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_load_balancer(self, lb_id: int) -> None:
        """Delete a load balancer."""
        response = requests.delete(
            f"{self.BASE_URL}/loadbalancers/{lb_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
    
    def create_listener(self,
                       lb_id: int,
                       protocol: str,
                       port: int,
                       name: Optional[str] = None) -> Dict:
        """Create a new listener for a load balancer."""
        data = {
            "protocol": protocol.upper(),
            "port": port
        }
        if name:
            data["name"] = name
            
        response = requests.post(
            f"{self.BASE_URL}/loadbalancers/{lb_id}/listeners",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def create_pool(self,
                   lb_id: int,
                   listener_id: int,
                   protocol: str,
                   method: str = "ROUND_ROBIN",
                   name: Optional[str] = None) -> Dict:
        """Create a new backend pool for a listener."""
        data = {
            "protocol": protocol.upper(),
            "method": method,
            "listener_id": listener_id
        }
        if name:
            data["name"] = name
            
        response = requests.post(
            f"{self.BASE_URL}/loadbalancers/{lb_id}/pools",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def add_member(self,
                  lb_id: int,
                  pool_id: int,
                  address: str,
                  port: int,
                  weight: int = 1) -> Dict:
        """Add a backend member to a pool."""
        data = {
            "address": address,
            "port": port,
            "weight": weight
        }
        response = requests.post(
            f"{self.BASE_URL}/loadbalancers/{lb_id}/pools/{pool_id}/members",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
