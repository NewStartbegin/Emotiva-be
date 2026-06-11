# 📋 Setup Checklist: Migrasi File Storage ke Supabase

Ikuti langkah-langkah di bawah untuk setup EMOTIVA-MATH dengan Supabase file storage.

## ✅ Step 1: Setup Supabase Project

- [ ] Buka https://supabase.com dan login/buat akun
- [ ] Create new project dengan nama `emotiva-math`
- [ ] Tunggu project selesai di-initialize

## ✅ Step 2: Create Storage Bucket

- [ ] Di Supabase Dashboard, pergi ke **Storage**
- [ ] Click **Create new bucket**
- [ ] Nama bucket: `materials`
- [ ] Set bucket ke **Public** (biar file bisa diakses publik)
- [ ] Click **Create bucket**

## ✅ Step 3: Get Supabase Credentials

- [ ] Di Dashboard, pergi ke **Project Settings**
- [ ] Click tab **API**
- [ ] Copy **Project URL** → `SUPABASE_URL` (contoh: https://xxxxx.supabase.co)
- [ ] Copy **Anon public key** → `SUPABASE_KEY`
- [ ] Copy **API Endpoint** untuk reference

## ✅ Step 4: Update Environment Variables

- [ ] Copy `.env.example` menjadi `.env`
- [ ] Edit `.env` dan tambahkan Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_BUCKET_NAME=materials
```

- [ ] Simpan file `.env`

## ✅ Step 5: Install Dependencies

```bash
# Masuk ke folder backend
cd be-emotiva-math

# Install requirements baru (supabase, python-multipart)
pip install -r requirements.txt
```

- [ ] Check instalasi berhasil tanpa error

## ✅ Step 6: Verify Setup dengan Test

### Test 1: Check Supabase Connection

```bash
python -c "
from app import create_app
from app.supabase_client import supabase_client

app = create_app()
with app.app_context():
    if supabase_client.client:
        print('✅ Supabase connected successfully!')
    else:
        print('❌ Supabase connection failed - check credentials')
"
```

- [ ] Output menunjukkan connection successful

### Test 2: Upload File Test

```bash
# Terminal di folder be-emotiva-math
python -c "
from app import create_app
from app.supabase_client import supabase_client
from werkzeug.datastructures import FileStorage
import io

app = create_app()
with app.app_context():
    # Create test file
    test_content = b'Test content untuk Supabase'
    test_file = FileStorage(
        stream=io.BytesIO(test_content),
        filename='test.txt',
        content_type='text/plain'
    )

    try:
        result = supabase_client.upload_file(
            test_file,
            'materials/kubus/test.txt',
            'test.txt'
        )
        print(f'✅ Upload successful: {result}')

        # Clean up
        supabase_client.delete_file('materials/kubus/test.txt')
        print('✅ Cleanup successful')
    except Exception as e:
        print(f'❌ Error: {e}')
"
```

- [ ] Upload berhasil dan bisa delete file

### Test 3: Run Flask App

```bash
python run.py
```

- [ ] Flask app berjalan tanpa error di port 5000
- [ ] Health check: `curl http://localhost:5000/api/health`

## ✅ Step 7: Test API Endpoints

### Test Upload Material

```bash
# Buat test file
echo "Materi Kubus: rumus volume = s³" > test_material.txt

# Upload via API
curl -X POST http://localhost:5000/api/materials \
  -F "judul=Materi Kubus" \
  -F "topik=kubus" \
  -F "level=pemula" \
  -F "created_by=Teacher1" \
  -F "file=@test_material.txt"
```

- [ ] Response status 201 (Created)
- [ ] Response termasuk `public_url`
- [ ] Material ID tercatat

### Test Get Materials

```bash
curl http://localhost:5000/api/materials?topik=kubus
```

- [ ] Response menunjukkan material yang baru diupload
- [ ] File path berisi `materials/kubus/`

### Test Download Material

```bash
# Ganti MATERIAL_ID dengan ID dari response sebelumnya
curl http://localhost:5000/api/materials/MATERIAL_ID/download -o downloaded.txt
cat downloaded.txt
```

- [ ] File terdownload dengan benar
- [ ] Content sesuai dengan yang diupload

## ✅ Step 8: Migrate Old Local Files (Optional)

Jika ada file lama di `uploads/materials/`:

```bash
python -c "
from app import create_app
from app.supabase_client import supabase_client
from app.models import TeacherMaterial, db
import os

app = create_app()
with app.app_context():
    UPLOAD_FOLDER = 'uploads/materials'

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
                db.session.rollback()
"
```

- [ ] Old files berhasil dimigrasikan
- [ ] Database records terupdate dengan Supabase paths

## ✅ Step 9: Verify RAG Service Works

```bash
python -c "
from app import create_app
from app.rag_service import rag_service

app = create_app()
with app.app_context():
    # Reload materials dari database
    rag_service.reload_materials()

    print(f'Materials loaded: {len(rag_service.materials_cache)}')
    print(f'Chunks created: {len(rag_service.chunks_cache)}')

    if rag_service.chunks_cache:
        print('✅ RAG service dapat membaca materials dari Supabase')
    else:
        print('⚠️ Tidak ada materials ditemukan')
"
```

- [ ] RAG service dapat load materials
- [ ] Chunks berhasil dibuat dari file Supabase

## ✅ Step 10: Final Verification

- [ ] Semua tests di atas passed
- [ ] Flask app berjalan normal di port 5000
- [ ] Upload, download, delete material bekerja
- [ ] RAG service dapat membaca materials
- [ ] No "Supabase client not initialized" errors

## 📝 Troubleshooting

### Error: "Supabase client not initialized"

→ Check `.env` file untuk SUPABASE_URL dan SUPABASE_KEY

### Error: "Failed to upload file"

→ Check:

- Bucket `materials` sudah created
- Bucket set ke Public
- SUPABASE_KEY valid

### Error: "File not found" saat download

→ File mungkin sudah dihapus atau path salah

### Port 5000 sudah digunakan

```bash
# Gunakan port lain
python run.py --port 5001
```

## 🎉 Selesai!

Aplikasi EMOTIVA-MATH sudah siap menggunakan Supabase untuk file storage!

### File-file yang Penting:

- `.env` - Environment variables dengan Supabase credentials
- `app/supabase_client.py` - Supabase client
- `app/config.py` - Konfigurasi Supabase
- `app/routes.py` - Updated endpoints untuk upload/download/delete
- `app/rag_service.py` - Updated untuk membaca dari Supabase
- `SUPABASE_SETUP.md` - Dokumentasi lengkap setup

### Dokumentasi:

- [SUPABASE_SETUP.md](./SUPABASE_SETUP.md) - Setup guide lengkap
- [MIGRATION_SUMMARY.md](./MIGRATION_SUMMARY.md) - Summary perubahan
- [.env.example](./.env.example) - Template environment variables

## 📞 Support

Jika ada masalah, check:

1. [Supabase Documentation](https://supabase.com/docs)
2. [SUPABASE_SETUP.md](./SUPABASE_SETUP.md) - Troubleshooting section
3. Print logs untuk debugging (debug prints ada di kode)
