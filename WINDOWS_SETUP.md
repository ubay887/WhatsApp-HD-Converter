# WhatsApp HD Converter - Windows Setup Guide

## ✅ Setup Selesai!

Semua yang dibutuhkan sudah terinstall:
- ✅ Python 3.13.0
- ✅ FFmpeg 8.1.1
- ✅ Flask & Dependencies
- ✅ Path sudah disesuaikan untuk Windows

## 🚀 Cara Menjalankan

### Opsi 1: Menggunakan Batch File (Paling Mudah)

1. Double-click file `start_server.bat`
2. Server akan jalan di `http://localhost:5000`
3. Tekan CTRL+C untuk stop server

### Opsi 2: Manual via Command Prompt

```cmd
cd C:\laragon\www\whatsapp-hd-converter
python app.py
```

Server akan jalan di:
- http://localhost:5000
- http://127.0.0.1:5000

## 🧪 Testing

### Test 1: Cek API berjalan dengan baik

Buka browser dan akses:
```
http://localhost:5000/health
```

Atau jalankan test script:
```cmd
python test_api.py
```

### Test 2: Upload dan konversi video

Gunakan test script yang sudah ada:
```cmd
python test_client.py
```

Atau test manual dengan curl:
```cmd
curl -X POST -F "video=@test_video.mp4" http://localhost:5000/convert --output converted.mp4
```

## 📁 Lokasi File Temporary

Video yang diupload dan hasil konversi disimpan di:
```
C:\Users\[USERNAME]\AppData\Local\Temp\whatsapp_converter\
├── uploads\   (file upload)
└── outputs\   (hasil konversi)
```

File otomatis dihapus setelah 1 jam.

## 🔧 Troubleshooting

### Server tidak bisa diakses
- Pastikan tidak ada aplikasi lain yang menggunakan port 5000
- Coba restart server
- Cek firewall Windows

### FFmpeg error
- Restart terminal/command prompt
- Cek FFmpeg terinstall: `ffmpeg -version`
- Jika belum terdeteksi, restart komputer

### Import error
- Pastikan dependencies terinstall: `pip install -r requirements.txt`
- Gunakan Python yang sama dengan yang digunakan untuk install dependencies

## 📱 Cara Menggunakan

### Dari Browser (Upload Manual)

1. Jalankan server
2. Buka Postman atau tools sejenis
3. POST ke `http://localhost:5000/convert`
4. Upload video dengan field name: `video`
5. Download hasil konversi

### Dari Python Script

```python
import requests

# Upload video
with open('video.mp4', 'rb') as f:
    files = {'video': f}
    response = requests.post('http://localhost:5000/convert', files=files)

# Save hasil
with open('converted.mp4', 'wb') as f:
    f.write(response.content)

print("Video berhasil dikonversi!")
```

### Dari Command Line (curl)

```cmd
curl -X POST -F "video=@input.mp4" http://localhost:5000/convert --output output.mp4
```

## 🌐 Akses dari Perangkat Lain (HP/Tablet)

Jika ingin akses dari HP di jaringan yang sama:

1. Cek IP komputer Windows:
   ```cmd
   ipconfig
   ```
   Cari "IPv4 Address", misalnya: `192.168.1.100`

2. Dari HP, akses:
   ```
   http://192.168.1.100:5000/convert
   ```

3. Pastikan Windows Firewall mengizinkan koneksi ke port 5000

## ⚙️ Konfigurasi

Edit `app.py` untuk mengubah:
- `MAX_FILE_SIZE`: Ukuran maksimal file (default 100MB)
- `ALLOWED_EXTENSIONS`: Format video yang diizinkan
- Port: Ubah di bagian bawah file (default 5000)

## 📊 Spesifikasi Output

Video hasil konversi:
- Format: MP4 (H.264 + AAC)
- Resolusi: 1080p (maintain aspect ratio)
- Video Bitrate: 5000 kbps
- Audio Bitrate: 192 kbps
- Durasi: Maksimal 30 detik
- Optimized untuk WhatsApp Status

## 🎯 Next Steps

1. Test dengan video kecil dulu (< 10MB)
2. Upload ke WhatsApp Status
3. Bandingkan kualitas dengan video original

## 💡 Tips

- Video lebih pendek = proses lebih cepat
- Gunakan video landscape untuk hasil terbaik
- Jangan upload video > 100MB
- Tutup aplikasi lain saat konversi video besar

## 📞 Support

Jika ada masalah:
1. Cek error message di terminal
2. Lihat log FFmpeg
3. Test dengan video yang lebih kecil
4. Restart server dan coba lagi

---

**Selamat mencoba! 🎉**
