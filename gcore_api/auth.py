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
            if response.status_code == 401:
                raise ValueError("Invalid or expired API token")
            elif response.status_code == 403:
                raise ValueError("Token lacks necessary permissions")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                if status_code == 401:
                    raise ValueError("Invalid or expired API token")
                elif status_code == 403:
                    raise ValueError("Token lacks necessary permissions")
                else:
                    raise ValueError(f"API request failed: {e}")
            raise ValueError("Failed to connect to Gcore API. Please check your internet connection.")
