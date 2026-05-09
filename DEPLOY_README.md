# 🚀 Quick Deployment Guide

## Recommended: Railway.app

### Why Railway?
- ✅ FFmpeg pre-installed
- ✅ No sleep time
- ✅ $5 free credit/month
- ✅ Easy deployment
- ✅ Auto SSL

### Quick Deploy (3 Steps)

#### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-hd-converter.git
git push -u origin main
```

#### 2. Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select **whatsapp-hd-converter**
5. Wait 2-3 minutes ⏳

#### 3. Get Your URL
1. Go to **Settings** → **Generate Domain**
2. Your app is live! 🎉
3. URL: `https://your-app.railway.app`

### Test Your Deployment
```bash
# Health check
curl https://your-app.railway.app/health

# Open in browser
https://your-app.railway.app
```

---

## Alternative: Render.com

### Quick Deploy

#### 1. Push to GitHub (same as above)

#### 2. Deploy on Render
1. Go to https://render.com
2. Click **New** → **Web Service**
3. Connect GitHub repository
4. Configure:
   - Environment: **Docker**
   - Plan: **Free**
5. Click **Create Web Service**
6. Wait 5-10 minutes ⏳

#### 3. Your URL
- URL: `https://whatsapp-hd-converter.onrender.com`

**Note:** Free tier sleeps after 15 minutes of inactivity

---

## Alternative: Fly.io

### Quick Deploy

#### 1. Install Fly CLI
**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

#### 2. Deploy
```bash
fly auth login
fly launch --no-deploy
fly deploy
fly open
```

---

## 🎯 Which One to Choose?

| Feature | Railway | Render | Fly.io |
|---------|---------|--------|--------|
| **Setup Time** | 3 min | 5 min | 5 min |
| **Free Tier** | $5 credit | 750 hrs | 3 VMs |
| **Sleep** | No | Yes | Auto |
| **FFmpeg** | ✅ | ✅ | ✅ |
| **Best For** | Production | Testing | Advanced |

**Recommendation:** Start with **Railway** for best experience.

---

## 📝 Files Included

- ✅ `Dockerfile` - Docker configuration
- ✅ `railway.toml` - Railway config
- ✅ `render.yaml` - Render config
- ✅ `fly.toml` - Fly.io config
- ✅ `Procfile` - Process configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `.dockerignore` - Docker ignore rules

---

## 🐛 Troubleshooting

### Build Failed
```bash
# Test locally
docker build -t whatsapp-converter .
docker run -p 8080:8080 whatsapp-converter
```

### FFmpeg Not Found
- Check Dockerfile includes FFmpeg installation
- Rebuild the app

### Out of Memory
- Reduce MAX_FILE_SIZE in app.py
- Upgrade to paid tier

---

## 📚 Full Documentation

See `DEPLOYMENT_GUIDE.md` for complete instructions.

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Platform account created
- [ ] App deployed successfully
- [ ] Health endpoint working (`/health`)
- [ ] Test video conversion
- [ ] Custom domain setup (optional)

---

## 🎉 Success!

Your app is now live and ready to convert videos!

**Share your URL:**
- Railway: `https://your-app.railway.app`
- Render: `https://whatsapp-hd-converter.onrender.com`
- Fly.io: `https://whatsapp-hd-converter.fly.dev`

---

## 💡 Pro Tips

1. **Monitor Usage:** Check `/storage` endpoint
2. **Cleanup:** Use `/cleanup` endpoint if needed
3. **Logs:** Check platform dashboard for errors
4. **Custom Domain:** Setup in platform settings
5. **Uptime:** Use UptimeRobot for monitoring

---

## 🆘 Need Help?

1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Check platform documentation
3. Open GitHub issue

---

**Made with ❤️ for WhatsApp Status HD Videos**
