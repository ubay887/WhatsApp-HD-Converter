# 🚀 Deployment Guide - WhatsApp HD Converter

## 📊 Platform Comparison

| Platform | Free Tier | FFmpeg | RAM | Storage | Sleep | Best For |
|----------|-----------|--------|-----|---------|-------|----------|
| **Railway** | $5 credit/month | ✅ | 512MB | 1GB | No | **RECOMMENDED** |
| **Render** | 750 hours/month | ✅ | 512MB | - | Yes (15min) | Good |
| **Fly.io** | 3 VMs free | ✅ | 256MB | 3GB | Auto scale | Good |
| **Heroku** | Deprecated | ❌ | - | - | - | Not recommended |

## 🏆 Recommended: Railway.app

**Pros:**
- ✅ FFmpeg pre-installed
- ✅ No sleep time
- ✅ Easy deployment
- ✅ $5 free credit/month
- ✅ Auto SSL
- ✅ Good performance

**Cons:**
- ⚠️ Credit-based (not unlimited)
- ⚠️ Need credit card for verification

---

## 🚂 Deploy to Railway

### Step 1: Prepare Repository

```bash
# Make sure you're in project directory
cd C:\laragon\www\whatsapp-hd-converter

# Initialize git if not already
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-hd-converter.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. **Sign up:** https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. **Select repository:** whatsapp-hd-converter
4. **Railway will auto-detect** Dockerfile and deploy
5. **Wait 2-3 minutes** for build to complete
6. **Generate domain:** Settings → Generate Domain
7. **Done!** Your app is live at: `https://your-app.railway.app`

### Step 3: Verify Deployment

```bash
# Check health
curl https://your-app.railway.app/health

# Check storage
curl https://your-app.railway.app/storage

# Test conversion
# Upload video via web interface
```

### Railway Configuration

**Environment Variables:** (Optional)
```
PORT=8080
DEBUG=false
MAX_FILE_SIZE=104857600
```

**Resources:**
- Memory: 512MB (default)
- CPU: Shared
- Disk: 1GB

---

## 🎨 Deploy to Render.com

### Step 1: Prepare Repository

Same as Railway (push to GitHub)

### Step 2: Deploy to Render

1. **Sign up:** https://render.com
2. **New** → **Web Service**
3. **Connect GitHub** repository
4. **Configure:**
   - Name: `whatsapp-hd-converter`
   - Environment: `Docker`
   - Plan: `Free`
   - Build Command: (auto-detected)
   - Start Command: (auto-detected)
5. **Create Web Service**
6. **Wait 5-10 minutes** for build
7. **Done!** Live at: `https://whatsapp-hd-converter.onrender.com`

### Render Configuration

**Environment Variables:**
```
PORT=8080
PYTHON_VERSION=3.12.0
```

**Important:**
- ⚠️ Free tier sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep takes 30-60 seconds
- ⚠️ 750 hours/month limit

---

## ✈️ Deploy to Fly.io

### Step 1: Install Fly CLI

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Deploy

```bash
# Login
fly auth login

# Launch app (will use fly.toml)
fly launch --no-deploy

# Deploy
fly deploy

# Open app
fly open
```

### Step 3: Configure

```bash
# Set secrets
fly secrets set DEBUG=false

# Scale memory (if needed)
fly scale memory 512

# View logs
fly logs

# Check status
fly status
```

### Fly.io Configuration

**Region:** Singapore (sin) - closest to Indonesia

**Resources:**
- Memory: 512MB
- CPU: Shared
- Storage: 3GB

---

## 🔧 Post-Deployment Setup

### 1. Test Endpoints

```bash
# Health check
curl https://your-app.com/health

# Storage info
curl https://your-app.com/storage

# API info
curl https://your-app.com/
```

### 2. Monitor Logs

**Railway:**
```
Dashboard → Deployments → View Logs
```

**Render:**
```
Dashboard → Logs
```

**Fly.io:**
```bash
fly logs
```

### 3. Setup Custom Domain (Optional)

**Railway:**
1. Settings → Domains
2. Add custom domain
3. Update DNS records

**Render:**
1. Settings → Custom Domain
2. Add domain
3. Update DNS

**Fly.io:**
```bash
fly certs add yourdomain.com
```

---

## 📊 Monitoring & Maintenance

### Check Storage Usage

```bash
curl https://your-app.com/storage
```

### Manual Cleanup

```bash
curl -X POST https://your-app.com/cleanup
```

### View Logs

**Railway:**
- Dashboard → Logs (real-time)

**Render:**
- Dashboard → Logs

**Fly.io:**
```bash
fly logs
fly logs -a whatsapp-hd-converter
```

### Restart Service

**Railway:**
- Dashboard → Deployments → Restart

**Render:**
- Dashboard → Manual Deploy → Clear build cache & deploy

**Fly.io:**
```bash
fly apps restart whatsapp-hd-converter
```

---

## 🐛 Troubleshooting

### Build Failed

**Check:**
1. Dockerfile syntax
2. requirements.txt dependencies
3. Python version compatibility

**Solution:**
```bash
# Test locally with Docker
docker build -t whatsapp-converter .
docker run -p 8080:8080 whatsapp-converter
```

### FFmpeg Not Found

**Railway/Render:** Should work automatically (Dockerfile installs FFmpeg)

**Fly.io:** Check Dockerfile includes FFmpeg installation

### Out of Memory

**Symptoms:**
- Conversion fails for large files
- App crashes during processing

**Solutions:**
1. Reduce MAX_FILE_SIZE
2. Upgrade to paid tier (more RAM)
3. Optimize FFmpeg settings (use "fast" preset)

### App Sleeping (Render)

**Problem:** Free tier sleeps after 15 minutes

**Solutions:**
1. Use Railway instead (no sleep)
2. Upgrade to paid tier ($7/month)
3. Use uptime monitoring service (ping every 10 minutes)

### Slow Conversion

**Check:**
1. FFmpeg preset (use "fast" or "medium")
2. Server resources
3. File size

**Optimize:**
```python
# In app.py, change preset
"-preset", "fast",  # Instead of "medium"
```

---

## 💰 Cost Estimation

### Railway (Recommended)

**Free Tier:**
- $5 credit/month
- ~500 hours runtime
- ~100-200 conversions/month

**Paid:**
- $5/month for 500 hours
- $0.01/hour after that

### Render

**Free Tier:**
- 750 hours/month
- Unlimited conversions (with sleep)

**Paid:**
- $7/month (no sleep)
- Unlimited conversions

### Fly.io

**Free Tier:**
- 3 VMs free
- 160GB bandwidth
- ~200-300 conversions/month

**Paid:**
- $1.94/month per VM
- $0.02/GB bandwidth

---

## 🎯 Best Practices

### 1. Environment Variables

```bash
# Production settings
PORT=8080
DEBUG=false
MAX_FILE_SIZE=104857600
ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Monitoring

- Setup uptime monitoring (UptimeRobot, Pingdom)
- Monitor storage usage
- Check logs regularly

### 3. Security

- Use HTTPS only
- Set CORS properly
- Limit file size
- Rate limiting (if needed)

### 4. Performance

- Use CDN for static files
- Enable gzip compression
- Optimize FFmpeg settings
- Auto cleanup files

---

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Dockerfile tested locally
- [ ] requirements.txt updated
- [ ] Environment variables configured
- [ ] Health endpoint working
- [ ] FFmpeg installed and working
- [ ] File cleanup working
- [ ] Custom domain setup (optional)
- [ ] Monitoring setup
- [ ] Backup plan ready

---

## 🆘 Support

### Railway
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

### Render
- Docs: https://render.com/docs
- Support: support@render.com

### Fly.io
- Docs: https://fly.io/docs
- Community: https://community.fly.io

---

## 🚀 Quick Deploy Commands

### Railway
```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Render
```bash
# Just push to GitHub
git push origin main
# Render auto-deploys
```

### Fly.io
```bash
# Install CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

---

## 📌 Important Notes

1. **FFmpeg Required:** All platforms must support FFmpeg
2. **File Size Limit:** Keep under 100MB for free tiers
3. **Timeout:** Set to 300 seconds for large files
4. **Storage:** Files auto-deleted after conversion
5. **RAM:** Minimum 512MB recommended

---

## ✅ Recommended Setup

**For Indonesia Users:**

1. **Platform:** Railway.app
2. **Region:** Singapore (closest)
3. **Plan:** Free tier ($5 credit)
4. **Domain:** Use Railway subdomain or custom
5. **Monitoring:** UptimeRobot (free)

**Total Cost:** $0/month (with free tier)

---

## 🎉 Success!

Your WhatsApp HD Converter is now live and ready to use!

**Next Steps:**
1. Share the URL with users
2. Monitor usage and logs
3. Setup custom domain (optional)
4. Add analytics (optional)

**Live URL Examples:**
- Railway: `https://whatsapp-hd-converter.railway.app`
- Render: `https://whatsapp-hd-converter.onrender.com`
- Fly.io: `https://whatsapp-hd-converter.fly.dev`
