# 🎬 WhatsApp HD Video Converter

![Version](https://img.shields.io/badge/version-1.0-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

Convert your videos to HD quality optimized for WhatsApp Status. Stop losing quality when uploading to WhatsApp!

## ✨ Features

- 🎯 **HD Quality Output** - 1080p resolution with 5Mbps bitrate
- ⚡ **Fast Processing** - Optimized FFmpeg settings for quick conversion
- 🎨 **Modern Web UI** - Beautiful, responsive interface
- 📱 **Mobile Friendly** - Works on desktop, tablet, and mobile
- 🔒 **100% Private** - Videos auto-deleted after 1 hour
- 💯 **Completely Free** - No limits, no registration required

## 🖼️ Screenshots

### Desktop View
![Desktop UI](https://via.placeholder.com/800x400/25D366/FFFFFF?text=Desktop+UI)

### Mobile View
![Mobile UI](https://via.placeholder.com/400x600/25D366/FFFFFF?text=Mobile+UI)

## 🚀 Quick Start

### Windows (Recommended)

1. **Clone or Download**
   ```cmd
   git clone https://github.com/yourusername/whatsapp-hd-converter.git
   cd whatsapp-hd-converter
   ```

2. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   ```cmd
   winget install --id=Gyan.FFmpeg -e --silent
   ```

4. **Start Server**
   ```cmd
   start_ui.bat
   ```
   Or manually:
   ```cmd
   python app.py
   ```

5. **Open Browser**
   ```
   http://localhost:5000
   ```

### Linux/Mac

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   
   # Install FFmpeg
   # Ubuntu/Debian:
   sudo apt-get install ffmpeg
   
   # macOS:
   brew install ffmpeg
   ```

2. **Update Paths** (if needed)
   Edit `app.py` and change temp folder paths if needed.

3. **Start Server**
   ```bash
   python app.py
   ```

4. **Open Browser**
   ```
   http://localhost:5000
   ```

## 📖 Documentation

- [Windows Setup Guide](WINDOWS_SETUP.md) - Detailed Windows installation
- [UI Guide](UI_GUIDE.md) - Web interface documentation
- [Deployment Guide](DEPLOYMENT.md) - Deploy to cloud platforms
- [API Documentation](#api-documentation) - API endpoints reference

## 🎯 How to Use

### Web Interface

1. Open http://localhost:5000 in your browser
2. Drag & drop your video or click to browse
3. Click "Convert to HD"
4. Wait for processing (10-60 seconds)
5. Download the optimized video
6. Upload to WhatsApp Status

### API Usage

```bash
# Upload and convert
curl -X POST \
  -F "video=@your-video.mp4" \
  http://localhost:5000/convert \
  --output optimized.mp4
```

### Python Script

```python
import requests

# Upload video
with open('video.mp4', 'rb') as f:
    files = {'video': f}
    response = requests.post('http://localhost:5000/convert', files=files)

# Save result
with open('converted.mp4', 'wb') as f:
    f.write(response.content)
```

## 📋 Technical Specifications

### Input
- **Max Size:** 100MB
- **Formats:** MP4, MOV, AVI, MKV, WEBM, M4V
- **Any resolution/bitrate**

### Output
- **Format:** MP4 (H.264 + AAC)
- **Resolution:** 1080p (maintains aspect ratio)
- **Video Bitrate:** 5000 kbps
- **Audio Bitrate:** 192 kbps
- **Max Duration:** 30 seconds
- **Codec:** H.264 (libx264)
- **Audio Codec:** AAC
- **Pixel Format:** yuv420p
- **CRF:** 18 (near-lossless quality)

## 🔧 Configuration

Edit `app.py` to customize:

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'm4v'}

# FFmpeg settings in optimize_for_whatsapp() function
```

## 🌐 API Documentation

### Endpoints

#### `GET /`
Returns the web interface

#### `GET /api`
Returns API information and usage instructions

**Response:**
```json
{
  "status": "online",
  "service": "WhatsApp HD Video Converter API",
  "version": "1.0",
  "ffmpeg_available": true,
  "endpoints": {...},
  "usage": {...}
}
```

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-09T16:30:00",
  "ffmpeg_available": true
}
```

#### `POST /convert`
Main conversion endpoint

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Field name: `video`
- Max size: 100MB

**Response:**
- Content-Type: `video/mp4`
- Body: Optimized video file

**Error Response:**
```json
{
  "error": "Error message here"
}
```

## 📊 Performance

Processing time depends on:
- Video length
- Input quality
- Server resources

Typical times:
- Small videos (<10MB): 5-15 seconds
- Medium videos (10-50MB): 15-45 seconds
- Large videos (50-100MB): 45-90 seconds

## 🐛 Troubleshooting

### Server won't start
- Check if port 5000 is available
- Verify Python is installed: `python --version`
- Check dependencies: `pip list`

### FFmpeg errors
- Verify FFmpeg is installed: `ffmpeg -version`
- Restart terminal/command prompt
- On Windows, restart computer after FFmpeg install

### Upload fails
- Check file size (max 100MB)
- Verify file format is supported
- Check server logs for errors

### Slow processing
- Use shorter videos (< 1 minute)
- Close other applications
- Check CPU usage

### UI not loading
- Clear browser cache (Ctrl+F5)
- Check browser console (F12) for errors
- Verify static files exist in `static/` folder

## 🔒 Security & Privacy

- Videos are stored temporarily only
- Automatic cleanup after 1 hour
- No permanent storage
- No user tracking or analytics
- CORS enabled for API access
- File size and type validation

## 📱 Mobile Access

Access from phone/tablet on same network:

1. Find your computer's IP:
   ```cmd
   ipconfig  # Windows
   ifconfig  # Linux/Mac
   ```

2. On mobile browser, visit:
   ```
   http://YOUR_IP:5000
   ```

3. Allow port 5000 in firewall if needed

## 🚀 Deployment

Deploy to cloud platforms:

- **Railway** (Recommended) - See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Render** - Free tier available
- **Heroku** - Easy deployment
- **DigitalOcean** - VPS option
- **AWS/GCP/Azure** - Enterprise options

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Video preview before conversion
- [ ] Batch processing
- [ ] Custom quality settings
- [ ] Video trimming
- [ ] Watermark support
- [ ] Dark mode
- [ ] Multi-language support
- [ ] PWA support
- [ ] Rate limiting
- [ ] User accounts (optional)

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- FFmpeg for video processing
- Flask for web framework
- WhatsApp for inspiration

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/whatsapp-hd-converter/issues)
- **Email:** your.email@example.com
- **Documentation:** See docs folder

## 🔗 Links

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [WhatsApp Status Specs](https://faq.whatsapp.com/)

---

**Made with ❤️ for better WhatsApp Status quality**

⭐ Star this repo if you find it useful!
