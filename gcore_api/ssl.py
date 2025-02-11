import requests
from typing import List, Dict, Optional
from datetime import datetime

class SSLClient:
    """Client for Gcore SSL Certificate API operations."""
    
    BASE_URL = "https://api.gcore.com/ssl/v1"
    
    def __init__(self, auth):
        self.auth = auth
    
    def list_certificates(self) -> List[Dict]:
        """List all SSL certificates."""
        response = requests.get(
            f"{self.BASE_URL}/certificates",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_certificate(self, cert_id: int) -> Dict:
        """Get details of a specific SSL certificate."""
        response = requests.get(
            f"{self.BASE_URL}/certificates/{cert_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def upload_certificate(self,
                         name: str,
                         cert: str,
                         private_key: str,
                         chain: Optional[str] = None) -> Dict:
        """Upload a custom SSL certificate."""
        data = {
            "name": name,
            "certificate": cert,
            "private_key": private_key
        }
        if chain:
            data["chain"] = chain
            
        response = requests.post(
            f"{self.BASE_URL}/certificates",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_certificate(self, cert_id: int) -> None:
        """Delete an SSL certificate."""
        response = requests.delete(
            f"{self.BASE_URL}/certificates/{cert_id}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
    
    def request_certificate(self, 
                          domains: List[str],
                          validation_method: str = "dns") -> Dict:
        """Request a new SSL certificate through Gcore."""
        data = {
            "domains": domains,
            "validation_method": validation_method
        }
        response = requests.post(
            f"{self.BASE_URL}/certificates/request",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def get_validation_status(self, cert_id: int) -> Dict:
        """Get domain validation status for a certificate request."""
        response = requests.get(
            f"{self.BASE_URL}/certificates/{cert_id}/validation",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
