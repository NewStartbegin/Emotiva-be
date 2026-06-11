# Ringkasan Perubahan: Migrasi File Storage ke Supabase

## 📋 Overview

File materials dalam aplikasi EMOTIVA-MATH telah dimigrasikan dari penyimpanan **lokal** (`uploads/materials/`) menjadi **cloud storage Supabase**. Ini menghilangkan ketergantungan pada penyimpanan lokal dan memberikan skalabilitas yang lebih baik.

## ✅ File yang Diubah/Dibuat

### 1. **requirements.txt** ✏️ DIUBAH

- Menambahkan dependency baru:
  - `supabase==2.3.4` - Python client untuk Supabase Storage
  - `python-multipart==0.0.6` - Support multipart form data

### 2. **app/config.py** ✏️ DIUBAH

- Menambahkan Supabase configuration:
  ```python
  SUPABASE_URL = os.environ.get('SUPABASE_URL')
  SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
  SUPABASE_BUCKET_NAME = os.environ.get('SUPABASE_BUCKET_NAME', 'materials')
  MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
  ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'}
  ```

### 3. **app/supabase_client.py** ✨ FILE BARU

File baru yang mengelola semua operasi Supabase:

- **SupabaseClient class** dengan methods:
  - `upload_file()` - Upload file ke bucket
  - `download_file()` - Download file dari bucket
  - `delete_file()` - Delete file dari bucket
  - `get_public_url()` - Get public URL
  - `list_files()` - List files di bucket
  - `file_exists()` - Check file existence
  - `_get_content_type()` - Get MIME type

### 4. **app/routes.py** ✏️ DIUBAH

- **Import baru**: `from app.supabase_client import supabase_client`
- **handle_materials() - POST method**:
  - ✅ Sebelum: `file.save(file_path)` (local)
  - ✅ Sesudah: `supabase_client.upload_file()` (cloud)
  - File disimpan dengan path: `materials/{topik}/{timestamp}_{filename}`
  - Database menyimpan Supabase path, bukan local path
- **download_material()**:
  - ✅ Sebelum: `send_from_directory()` (local file serving)
  - ✅ Sesudah: `supabase_client.download_file()` (streaming dari Supabase)
  - Return file dengan proper content-type headers
- **handle_material_detail() - DELETE method**:
  - ✅ Sebelum: `os.remove(file_path)` (local deletion)
  - ✅ Sesudah: `supabase_client.delete_file()` (delete dari bucket)

### 5. **app/rag_service.py** ✏️ DIUBAH

- **Import baru**: `from app.supabase_client import supabase_client`
- **\_extract_content() method**:
  - ✅ Sebelum: `os.path.exists()` + `open()` (local file reading)
  - ✅ Sesudah: `supabase_client.download_file()` (download dari Supabase)
  - Support untuk TXT dan PDF files dari Supabase
  - Fallback ke `konten` field jika ada error
- **get_material_by_topik() method**:
  - Sekarang konsisten menggunakan `_extract_content()` untuk kedua source (Supabase & konten field)

### 6. **SUPABASE_SETUP.md** ✨ FILE BARU

Dokumentasi lengkap setup Supabase:

- Cara mendapatkan credentials
- Setup bucket di Supabase
- Struktur folder di bucket
- Migration script untuk file lama
- Testing endpoints
- Troubleshooting

## 📊 Diagram Alur

### Sebelum (Local Storage)

```
Upload → Local Directory (uploads/materials/) → Database (file_path = local_path)
Download → Read Local File → Send Response
Delete → Delete Local File + Delete DB Record
```

### Sesudah (Supabase Cloud Storage)

```
Upload → Supabase Bucket (materials/topik/file) → Database (file_path = supabase_path)
Download → Download dari Supabase → Send Response
Delete → Delete dari Supabase Bucket + Delete DB Record
```

## 🔧 Configuration yang Diperlukan

**File `.env`**:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_BUCKET_NAME=materials
```

## 📦 Struktur File di Supabase Bucket

```
materials/
├── kubus/
│   ├── 20240101_120000_materi_kubus_1.pdf
│   ├── 20240101_120100_kubus_properties.txt
│   └── ...
├── balok/
│   ├── 20240101_120200_balok_volume.pdf
│   └── ...
├── bola/
├── tabung/
├── kerucut/
├── limas/
└── prisma/
```

## 🔄 Perubahan Database

**TeacherMaterial Model** - Tidak ada perubahan struktur, hanya interpretasi:

- `file_path` sebelum: `uploads/materials/20240101_120000_file.pdf` (local)
- `file_path` sesudah: `materials/kubus/20240101_120000_file.pdf` (Supabase path)

## ✨ Keuntungan Migrasi

| Aspek       | Lokal         | Supabase         |
| ----------- | ------------- | ---------------- |
| Scalability | Terbatas disk | Unlimited        |
| Backup      | Manual        | Automatic        |
| Akses       | Server only   | Global CDN       |
| Cost        | Infrastruktur | Pay-as-you-go    |
| Maintenance | Manual        | Managed          |
| Security    | Basic         | Enterprise-grade |

## 🚀 Testing Checklist

- [ ] Install dependencies: `pip install supabase python-multipart`
- [ ] Set environment variables (SUPABASE_URL, SUPABASE_KEY)
- [ ] Create bucket di Supabase dengan nama `materials`
- [ ] Test upload material via API
- [ ] Test download material file
- [ ] Test delete material
- [ ] Test RAG service membaca file dari Supabase
- [ ] Test LLM generation dengan materials dari Supabase

## ⚠️ Catatan Penting

1. **Old Local Files**: File lama di `uploads/materials/` masih ada. Bisa di-migrate menggunakan script di SUPABASE_SETUP.md

2. **Database Migration**: Tidak perlu migration database, tapi file_path akan berisi Supabase path untuk file baru

3. **Fallback**: Jika Supabase tidak connected, sistem fallback ke `konten` field

4. **Public URLs**: Semua file di bucket `materials` bersifat public untuk memudahkan akses

## 📝 Migrasi File Lama (Optional)

Jika ingin memindahkan file lama dari lokal ke Supabase:

```bash
python -c "
from app.supabase_client import supabase_client
from app.models import TeacherMaterial, db
from app import create_app
import os

app = create_app()
with app.app_context():
    for material in TeacherMaterial.query.all():
        if material.file_path and os.path.exists(material.file_path):
            try:
                with open(material.file_path, 'rb') as f:
                    supabase_path = f'materials/{material.topik}/{os.path.basename(material.file_path)}'
                    supabase_client.upload_file(f, supabase_path, material.file_name)
                    material.file_path = supabase_path
                    db.session.commit()
                    print(f'✅ Migrated: {material.file_name}')
            except Exception as e:
                print(f'❌ Error: {e}')
"
```

## 🔗 Links

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [Setup Guide](./SUPABASE_SETUP.md)
