import os
import mimetypes
import requests
from typing import List, Dict, Optional, BinaryIO
from pathlib import Path

class StorageClient:
    """Client for Gcore Storage API operations."""
    
    BASE_URL = "https://api.gcore.com/storage/v1"
    
    def __init__(self, auth):
        self.auth = auth
    
    def list_buckets(self) -> List[Dict]:
        """List all storage buckets."""
        response = requests.get(
            f"{self.BASE_URL}/buckets",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_bucket(self, 
                     name: str,
                     location: str = "eu-north-1",
                     access: str = "private") -> Dict:
        """Create a new storage bucket."""
        data = {
            "name": name,
            "location": location,
            "access": access
        }
        response = requests.post(
            f"{self.BASE_URL}/buckets",
            headers=self.auth.get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_bucket(self, bucket_name: str) -> None:
        """Delete a storage bucket."""
        response = requests.delete(
            f"{self.BASE_URL}/buckets/{bucket_name}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
    
    def list_objects(self, 
                    bucket_name: str,
                    prefix: Optional[str] = None,
                    delimiter: Optional[str] = None) -> Dict:
        """List objects in a bucket."""
        params = {}
        if prefix:
            params["prefix"] = prefix
        if delimiter:
            params["delimiter"] = delimiter
            
        response = requests.get(
            f"{self.BASE_URL}/buckets/{bucket_name}/objects",
            headers=self.auth.get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def upload_object(self,
                     bucket_name: str,
                     object_name: str,
                     file_path: str,
                     content_type: Optional[str] = None) -> Dict:
        """Upload an object to a bucket."""
        if not content_type:
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
        headers = self.auth.get_headers()
        headers['Content-Type'] = content_type
        
        with open(file_path, 'rb') as f:
            response = requests.put(
                f"{self.BASE_URL}/buckets/{bucket_name}/objects/{object_name}",
                headers=headers,
                data=f
            )
        response.raise_for_status()
        return response.json()
    
    def download_object(self,
                       bucket_name: str,
                       object_name: str,
                       file_path: Optional[str] = None) -> None:
        """Download an object from a bucket."""
        response = requests.get(
            f"{self.BASE_URL}/buckets/{bucket_name}/objects/{object_name}",
            headers=self.auth.get_headers(),
            stream=True
        )
        response.raise_for_status()
        
        if not file_path:
            file_path = os.path.basename(object_name)
            
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def delete_object(self, bucket_name: str, object_name: str) -> None:
        """Delete an object from a bucket."""
        response = requests.delete(
            f"{self.BASE_URL}/buckets/{bucket_name}/objects/{object_name}",
            headers=self.auth.get_headers()
        )
        response.raise_for_status()
