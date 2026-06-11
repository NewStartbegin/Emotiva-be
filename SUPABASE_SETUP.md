# Supabase Setup untuk EMOTIVA-MATH

## Deskripsi

File materials untuk EMOTIVA-MATH telah dipindahkan dari penyimpanan lokal ke **Supabase Storage Bucket**. Ini memberikan beberapa keuntungan:

- ✅ Scalable cloud storage
- ✅ Automatic backup
- ✅ Global CDN support
- ✅ Security & access control

## Environment Variables yang Diperlukan

Tambahkan ke file `.env` atau konfigurasi environment Anda:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_BUCKET_NAME=materials
```

### Cara Mendapatkan Credentials:

1. **Login ke Supabase Dashboard**: https://supabase.com
2. **Buka Project Settings** → **API**
3. **Copy URL** → `SUPABASE_URL`
4. **Copy Anonymous Key** (anon public) → `SUPABASE_KEY`

## Setup Bucket di Supabase

1. Di Supabase Dashboard, pergi ke **Storage**
2. **Create new bucket** dengan nama `materials`
3. Set bucket ke **Public** (agar file bisa di-download)
4. Pastikan bucket policies mengizinkan public access

## Struktur Folder di Bucket

File akan disimpan dengan struktur:

```
materials/
  ├── kubus/
  │   ├── 20240101_120000_file1.pdf
  │   └── 20240101_120100_file2.txt
  ├── balok/
  │   └── 20240101_120200_file3.pdf
  └── ...
```

## Instalasi Dependencies

```bash
pip install -r requirements.txt
```

Package baru yang ditambahkan:

- `supabase==2.3.4` - Python client untuk Supabase
- `python-multipart==0.0.6` - For multipart form data handling

## API Endpoints yang Berubah

### Upload Material (POST /api/materials)

- File sekarang diupload ke Supabase bucket
- Response termasuk `public_url` untuk akses langsung

### Download Material (GET /api/materials/<id>/download)

- Download langsung dari Supabase bucket
- Support streaming untuk file besar

### Delete Material (DELETE /api/materials/<id>)

- File dihapus dari Supabase bucket
- Database record juga dihapus

## Migrasi File dari Local ke Supabase (Optional)

Jika ada file lama di `uploads/materials/`, bisa dimigrasikan dengan script:

```python
from app.supabase_client import supabase_client
from app.models import TeacherMaterial
import os

# Script untuk migrate existing files
UPLOAD_FOLDER = 'uploads/materials'

for material in TeacherMaterial.query.all():
    if material.file_path and os.path.exists(material.file_path):
        try:
            with open(material.file_path, 'rb') as f:
                # Upload ke Supabase
                supabase_file_path = f"materials/{material.topik}/{os.path.basename(material.file_path)}"
                supabase_client.upload_file(f, supabase_file_path, material.file_name)

                # Update database
                material.file_path = supabase_file_path
                db.session.commit()
                print(f"✅ Migrated: {material.file_name}")
        except Exception as e:
            print(f"❌ Error migrating {material.file_name}: {e}")
```

## Troubleshooting

### Error: "Supabase client not initialized"

- Check SUPABASE_URL dan SUPABASE_KEY di environment variables
- Pastikan credentials benar

### Error: "Failed to upload file"

- Pastikan bucket sudah dibuat dengan nama `materials`
- Check bucket policies untuk public access

### Error: "File not found" saat download

- Pastikan file masih ada di Supabase bucket
- Check file path di database

## Testing

```bash
# Test upload
curl -X POST http://localhost:5000/api/materials \
  -F "judul=Test Material" \
  -F "topik=kubus" \
  -F "level=pemula" \
  -F "created_by=Teacher1" \
  -F "file=@/path/to/file.pdf"

# Test download
curl http://localhost:5000/api/materials/1/download -o downloaded_file.pdf

# Test list materials
curl http://localhost:5000/api/materials
```

## Reference

- [Supabase Storage Docs](https://supabase.com/docs/guides/storage)
- [Python Supabase Client](https://github.com/supabase-community/supabase-py)
