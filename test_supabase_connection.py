import os
from dotenv import load_dotenv
load_dotenv()

print("=== Supabase Connection Test ===")
print(f"URL: {os.getenv('SUPABASE_URL')}")
print(f"Bucket: {os.getenv('SUPABASE_BUCKET_NAME')}")
print()

try:
    from supabase import create_client
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    client = create_client(url, key)
    print("✅ Supabase client created successfully")
    
    # Try to list buckets
    print("\nTrying to list buckets...")
    buckets = client.storage.list_buckets()
    print(f"✅ Buckets found: {len(buckets)}")
    for bucket in buckets:
        print(f"  - {bucket.name}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
