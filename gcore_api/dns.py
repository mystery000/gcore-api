import requests
from typing import List, Dict, Optional, Union

class DNSClient:
    """Client for Gcore DNS API operations."""
    
    BASE_URL = "https://api.gcore.com/dns/v2"
    
    def __init__(self, auth):
        self.auth = auth
    
    def list_zones(self) -> List[Dict]:
        """List all DNS zones."""
        response = requests.get(
            f"{self.BASE_URL}/zones",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_zone(self, zone_id: int) -> Dict:
        """Get details of a specific DNS zone."""
        response = requests.get(
            f"{self.BASE_URL}/zones/{zone_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_zone(self, name: str) -> Dict:
        """Create a new DNS zone."""
        data = {"name": name}
        response = requests.post(
            f"{self.BASE_URL}/zones",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_zone(self, zone_id: int) -> None:
        """Delete a DNS zone."""
        response = requests.delete(
            f"{self.BASE_URL}/zones/{zone_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
    
    def list_records(self, zone_id: int) -> List[Dict]:
        """List all records in a DNS zone."""
        response = requests.get(
            f"{self.BASE_URL}/zones/{zone_id}/records",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_record(self, 
                     zone_id: int,
                     name: str,
                     type: str,
                     content: Union[str, List[str]],
                     ttl: int = 3600) -> Dict:
        """Create a new DNS record."""
        data = {
            "name": name,
            "type": type.upper(),
            "content": content,
            "ttl": ttl
        }
        response = requests.post(
            f"{self.BASE_URL}/zones/{zone_id}/records",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_record(self, zone_id: int, record_id: int) -> None:
        """Delete a DNS record."""
        response = requests.delete(
            f"{self.BASE_URL}/zones/{zone_id}/records/{record_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
