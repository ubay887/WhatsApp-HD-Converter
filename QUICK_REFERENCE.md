# ⚡ Quick Reference Card

## 🚀 Deploy in 3 Steps

```bash
# 1. Push to GitHub
git push origin main

# 2. Deploy on Railway
# Go to railway.app → New Project → Deploy from GitHub

# 3. Test
curl https://your-app.railway.app/health
```

## 📁 Essential Files

```
✅ app.py              - Main application
✅ Dockerfile          - Docker config
✅ requirements.txt    - Dependencies
✅ railway.toml        - Railway config
✅ templates/index.html - UI
```

## 🎯 Platform Comparison

| Platform | Free Tier | Sleep | Setup |
|----------|-----------|-------|-------|
| Railway  | $5 credit | No    | 3 min |
| Render   | 750 hrs   | Yes   | 5 min |
| Fly.io   | 3 VMs     | Auto  | 5 min |

**Recommended:** Railway

## 🔗 API Endpoints

```bash
GET  /              # Home page
GET  /health        # Health check
POST /convert       # Convert video
GET  /download/:id  # Download video
GET  /storage       # Storage info
POST /cleanup       # Manual cleanup
```

## 🧪 Test Commands

```bash
# Health check
curl https://your-app.com/health

# Storage info
curl https://your-app.com/storage

# Manual cleanup
curl -X POST https://your-app.com/cleanup
```

## 📊 Features

- ✅ FFmpeg video conversion
- ✅ Auto file cleanup
- ✅ Real-time progress
- ✅ Mobile responsive
- ✅ No external dependencies

## 🐛 Quick Fixes

**Build failed?**
```bash
docker build -t test .
```

**FFmpeg error?**
- Check Dockerfile includes FFmpeg

**Out of memory?**
- Reduce MAX_FILE_SIZE
- Upgrade tier

## 📚 Documentation

- **Quick Start:** DEPLOY_README.md
- **Complete Guide:** DEPLOYMENT_GUIDE.md
- **Cleanup System:** CLEANUP_SYSTEM.md

## 🎯 Deployment Scripts

```bash
# Windows
deploy.bat
verify-deployment.bat

# Linux/Mac
./deploy.sh
./verify-deployment.sh
```

## 💡 Pro Tips

1. Use Railway for production
2. Monitor logs after deploy
3. Test with different video formats
4. Setup custom domain
5. Use UptimeRobot for monitoring

## 🆘 Support

- Railway: https://discord.gg/railway
- Render: support@render.com
- Fly.io: https://community.fly.io

---

**Ready to deploy? Run:** `deploy.bat` or `./deploy.sh`
