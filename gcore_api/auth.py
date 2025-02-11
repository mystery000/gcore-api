import os
import requests
from typing import Optional

class GcoreAuth:
    """Handle authentication for Gcore API."""
    
    BASE_URL = "https://api.gcore.com"
    
    def __init__(self, api_token: Optional[str] = None):
        """Initialize auth handler.
        
        Args:
            api_token: Permanent API token. If not provided, will try to get from environment.
        """
        self.api_token = api_token or os.environ.get("GCORE_API_TOKEN")
        if not self.api_token:
            raise ValueError("API token must be provided or set in GCORE_API_TOKEN environment variable")
    
    def get_headers(self) -> dict:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def validate_token(self) -> bool:
        """Validate the API token by making a test request."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/iam/v1/auth/jwt/verify",
                headers=self.get_headers()
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
