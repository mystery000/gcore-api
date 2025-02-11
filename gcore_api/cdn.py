import requests
from typing import List, Dict, Optional
from .auth import GcoreAuth

class CDNClient:
    """Client for Gcore CDN API operations."""
    
    BASE_URL = "https://api.gcore.com/cdn/v1"
    
    def __init__(self, auth: GcoreAuth):
        self.auth = auth
    
    def list_resources(self) -> List[Dict]:
        """List all CDN resources."""
        response = requests.get(
            f"{self.BASE_URL}/resources",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_resource(self, resource_id: int) -> Dict:
        """Get details of a specific CDN resource."""
        response = requests.get(
            f"{self.BASE_URL}/resources/{resource_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_resource(self, 
                       origin: str,
                       cname: Optional[str] = None,
                       ssl: bool = True) -> Dict:
        """Create a new CDN resource."""
        data = {
            "origin": origin,
            "ssl": ssl
        }
        if cname:
            data["cname"] = cname
            
        response = requests.post(
            f"{self.BASE_URL}/resources",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
