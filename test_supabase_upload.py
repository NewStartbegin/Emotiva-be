import os
from dotenv import load_dotenv
import io

load_dotenv()

print("=== Test Upload ke Supabase ===")

try:
    from supabase import create_client
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    bucket_name = os.getenv('SUPABASE_BUCKET_NAME', 'materials')
    
    client = create_client(url, key)
    print(f"✅ Client created")
    print(f"Bucket: {bucket_name}")
    print()
    
    # Create test file
    test_content = b"Test material content untuk Kubus"
    test_path = f"{bucket_name}/kubus/test_material.txt"
    
    print(f"Attempting to upload to: {test_path}")
    
    # Try upload
    response = client.storage.from_(bucket_name).upload(
        path=f"kubus/test_material.txt",
        file=test_content
    )
    
    print(f"✅ Upload successful!")
    print(f"Response: {response}")
    
    # Get public URL
    public_url = client.storage.from_(bucket_name).get_public_url(f"kubus/test_material.txt")
    print(f"✅ Public URL: {public_url}")
    
    # Try download
    print("\nTrying to download...")
    data = client.storage.from_(bucket_name).download(f"kubus/test_material.txt")
    print(f"✅ Download successful!")
    print(f"Content: {data.decode('utf-8')}")
    
    # Cleanup - delete test file
    print("\nCleaning up...")
    client.storage.from_(bucket_name).remove([f"kubus/test_material.txt"])
    print(f"✅ Test file deleted")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
