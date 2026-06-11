# Menggunakan base image Python 3.9 (sesuai dengan versi venv kamu sebelumnya) yang ringan
FROM python:3.9-slim

# Menentukan folder kerja di dalam container
WORKDIR /app

# Mengcopy file requirements.txt terlebih dahulu (untuk optimasi cache Docker)
COPY requirements.txt .

# Tambahkan baris ini sebelum install requirements
RUN pip install --upgrade pip setuptools wheel

# Menginstal semua library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Mengcopy seluruh file proyek ke dalam container
COPY . .

# Membuka port 5000 agar bisa diakses dari luar container
EXPOSE 5000

# Perintah default untuk menjalankan Flask saat container menyala
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
