"""
Supabase Client untuk File Storage
Mengelola upload, download, dan delete file ke Supabase Storage Bucket
"""
import os
from supabase import create_client, Client
from typing import Optional, BinaryIO
import io


class SupabaseClient:
    """
    Client untuk mengelola file storage di Supabase
    """
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.bucket_name = os.environ.get('SUPABASE_BUCKET_NAME', 'materials')
        
        if not self.supabase_url or not self.supabase_key:
            print("⚠️  Warning: SUPABASE_URL or SUPABASE_KEY not configured")
            self.client: Optional[Client] = None
        else:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                print(f"✅ Supabase client initialized with bucket: {self.bucket_name}")
            except Exception as e:
                print(f"❌ Failed to initialize Supabase client: {e}")
                self.client = None
    
    def upload_file(self, file: BinaryIO, file_path: str, file_name: str) -> dict:
        """
        Upload file ke Supabase bucket
        
        Args:
            file: File object (dari request.files)
            file_path: Path di bucket (e.g., "materials/20240101_120000_filename.pdf")
            file_name: Original filename
        
        Returns:
            dict dengan status dan URL file
        """
        if not self.client:
            raise Exception("Supabase client not initialized. Check SUPABASE_URL and SUPABASE_KEY")
        
        try:
            # Read file content
            file_content = file.read()
            
            # Upload ke Supabase
            response = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": self._get_content_type(file_name)}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            
            print(f"✅ File uploaded successfully: {file_path}")
            
            return {
                'status': 'success',
                'file_path': file_path,
                'file_name': file_name,
                'public_url': public_url,
                'bucket': self.bucket_name
            }
        
        except Exception as e:
            print(f"❌ Error uploading file: {e}")
            raise Exception(f"Failed to upload file to Supabase: {str(e)}")
    
    def download_file(self, file_path: str) -> bytes:
        """
        Download file dari Supabase bucket
        
        Args:
            file_path: Path di bucket
        
        Returns:
            bytes: File content
        """
        if not self.client:
            raise Exception("Supabase client not initialized")
        
        try:
            # Download file
            response = self.client.storage.from_(self.bucket_name).download(file_path)
            
            print(f"✅ File downloaded successfully: {file_path}")
            return response
        
        except Exception as e:
            print(f"❌ Error downloading file: {e}")
            raise Exception(f"Failed to download file from Supabase: {str(e)}")
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file dari Supabase bucket
        
        Args:
            file_path: Path di bucket
        
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        if not self.client:
            raise Exception("Supabase client not initialized")
        
        try:
            # Delete file
            self.client.storage.from_(self.bucket_name).remove([file_path])
            
            print(f"✅ File deleted successfully: {file_path}")
            return True
        
        except Exception as e:
            print(f"⚠️  Error deleting file: {e}")
            return False
    
    def get_public_url(self, file_path: str) -> str:
        """
        Get public URL untuk file
        
        Args:
            file_path: Path di bucket
        
        Returns:
            str: Public URL
        """
        if not self.client:
            raise Exception("Supabase client not initialized")
        
        try:
            url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            return url
        except Exception as e:
            print(f"❌ Error getting public URL: {e}")
            return ""
    
    def list_files(self, prefix: str = "") -> list:
        """
        List files di bucket
        
        Args:
            prefix: Optional prefix untuk filter
        
        Returns:
            list: List of files
        """
        if not self.client:
            raise Exception("Supabase client not initialized")
        
        try:
            files = self.client.storage.from_(self.bucket_name).list(prefix)
            return files
        except Exception as e:
            print(f"❌ Error listing files: {e}")
            return []
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists
        
        Args:
            file_path: Path di bucket
        
        Returns:
            bool: True jika file exists, False jika tidak
        """
        if not self.client:
            return False
        
        try:
            files = self.client.storage.from_(self.bucket_name).list(file_path)
            return len(files) > 0
        except Exception as e:
            return False
    
    def _get_content_type(self, filename: str) -> str:
        """
        Get content type berdasarkan file extension
        
        Args:
            filename: Nama file
        
        Returns:
            str: Content type
        """
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        content_types = {
            'pdf': 'application/pdf',
            'txt': 'text/plain',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'ppt': 'application/vnd.ms-powerpoint',
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        
        return content_types.get(ext, 'application/octet-stream')


# Global instance
supabase_client = SupabaseClient()
