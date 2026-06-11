import requests
import io

# Test upload material via Flask API
BASE_URL = "http://localhost:5000"

print("=== Test Upload Material via Flask API ===\n")

# Create test file
test_content = b"Materi Kubus:\n\nKubus adalah bangun ruang dengan 6 sisi berbentuk persegi.\nRumus volume: V = s³\nRumus luas permukaan: L = 6s²"
test_file = io.BytesIO(test_content)

# Prepare form data
files = {
    'file': ('materi_kubus.txt', test_file, 'text/plain')
}

data = {
    'judul': 'Materi Kubus - Volume dan Luas Permukaan',
    'topik': 'kubus',
    'level': 'pemula',
    'created_by': 'Teacher1'
}

try:
    print(f"POST {BASE_URL}/api/materials")
    print(f"Data: {data}\n")
    
    response = requests.post(
        f"{BASE_URL}/api/materials",
        files=files,
        data=data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{response.json()}\n")
    
    if response.status_code == 201:
        print("✅ Upload successful!")
        material_id = response.json()['data']['id']
        print(f"Material ID: {material_id}")
        
        # Try to get the material
        print(f"\nTrying to GET material...")
        get_response = requests.get(f"{BASE_URL}/api/materials/{material_id}")
        print(f"GET Response: {get_response.json()}\n")
        
        # Try to download
        print(f"Trying to download material...")
        download_response = requests.get(f"{BASE_URL}/api/materials/{material_id}/download")
        if download_response.status_code == 200:
            print(f"✅ Download successful!")
            print(f"Content: {download_response.text}\n")
        else:
            print(f"❌ Download failed: {download_response.status_code}\n")
    else:
        print("❌ Upload failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
