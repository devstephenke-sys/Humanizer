# Complete Deployment Guide - Draftwell

This guide will walk you through deploying the entire Draftwell application to production.

## Overview

- **Frontend**: Vercel (https://vercel.com)
- **Backend**: Render (https://render.com)
- **Database**: Neon PostgreSQL (https://neon.tech) or SQLite
- **AI Provider**: OpenAI, Anthropic, or Ollama

## Prerequisites

1. **GitHub Account**: For hosting your code
2. **Vercel Account**: For frontend deployment
3. **Render Account**: For backend deployment
4. **Neon Account** (optional): For PostgreSQL database
5. **AI Provider API Key**: OpenAI, Anthropic, or Ollama

---

## Step 1: Prepare Your Code Repository

### 1.1 Push Code to GitHub

```bash
# Initialize git if not already done
cd C:\Users\DBTECH AFRICA\Desktop\Humanizer
git init
git add .
git commit -m "Initial commit - Draftwell AI writing workspace"

# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/draftwell.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Project Structure

Your repository should have this structure:

```
Humanizer/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vercel.json
├── .env.example
├── README.md
├── DEPLOYMENT.md
└── ARCHITECTURE.md
```

---

## Step 2: Deploy Backend (Render)

### 2.1 Sign Up for Render

1. Go to https://render.com
2. Sign up/login with GitHub
3. Verify your email

### 2.2 Create a New Web Service

1. Click **"New +"** in the top right
2. Select **"Web Service"**
3. Click **"Connect GitHub"** and authorize
4. Select your `draftwell` repository
5. Configure the service:

**Basic Settings:**
- **Name**: `draftwell-api`
- **Region**: Choose the region closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Instance Type**: Free (for testing) or Standard ($7/month for production)

### 2.3 Add Environment Variables

Scroll down to **"Environment"** section and add these variables:

```env
ENVIRONMENT=production
SECRET_KEY=generate-a-long-random-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database - Choose ONE:
# Option A: SQLite (simpler, no extra service needed)
DATABASE_URL=sqlite+aiosqlite:///./draftwell.db

# Option B: Neon PostgreSQL (recommended for production)
# Get this from Neon after Step 3
# DATABASE_URL=postgresql://user:password@ep-cool-name.us-east-2.aws.neon.tech/neondb?sslmode=require

# CORS - Add your Vercel domain later
CORS_ORIGINS=https://your-domain.vercel.app

# AI Provider - Choose ONE:
AI_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

# OR for Anthropic:
# AI_PROVIDER=anthropic
# ANTHROPIC_API_KEY=your-anthropic-api-key
# ANTHROPIC_MODEL=claude-3-5-haiku-latest

# OR for Ollama (local):
# AI_PROVIDER=ollama
# OLLAMA_BASE_URL=http://127.0.0.1:11434
# OLLAMA_MODEL=llama3.1

# Rate limiting (abuse protection, not paid quotas)
MAX_INPUT_CHARS=60000
RATE_LIMIT_WRITES=40
RATE_LIMIT_WINDOW_SECONDS=600
```

**How to generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.4 Deploy

Click **"Create Web Service"** and wait for deployment (2-5 minutes).

Render will provide a URL like:
```
https://draftwell-api.onrender.com
```

**Copy this URL** - you'll need it for the frontend configuration.

### 2.5 Test the Backend

Visit `https://draftwell-api.onrender.com/docs` to see the API documentation (Swagger UI).

---

## Step 3: Set Up Database (Optional - Neon PostgreSQL)

Skip this step if you're using SQLite (simpler for testing).

### 3.1 Sign Up for Neon

1. Go to https://neon.tech
2. Sign up/login
3. Create a new project

### 3.2 Get Connection String

1. In Neon dashboard, go to your project
2. Copy the **Connection String** (use the "Pooling" version)
3. It looks like: `postgresql://user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require`

### 3.3 Update Render Environment Variables

1. Go back to your Render service
2. Scroll to **"Environment"**
3. Update `DATABASE_URL` with your Neon connection string
4. Click **"Save Changes"**
5. Render will automatically redeploy

---

## Step 4: Deploy Frontend (Vercel)

### 4.1 Sign Up for Vercel

1. Go to https://vercel.com
2. Sign up/login with GitHub
3. Verify your email

### 4.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Select your `draftwell` repository
3. Configure the project:

**Framework Preset**: Vite

**Root Directory**: `frontend`

**Build Command**: `npm install && npm run build`

**Output Directory**: `dist`

### 4.3 Add Environment Variables

Scroll to **"Environment Variables"** and add:

```env
VITE_API_URL=https://draftwell-api.onrender.com
```

Replace with your actual Render backend URL from Step 2.

### 4.4 Deploy

Click **"Deploy"** and wait for deployment (1-2 minutes).

Vercel will provide a URL like:
```
https://draftwell-xyz.vercel.app
```

### 4.5 Update CORS in Backend

1. Go back to Render
2. Update `CORS_ORIGINS` environment variable:
```env
CORS_ORIGINS=https://draftwell-xyz.vercel.app
```
3. Save and let it redeploy

---

## Step 5: Configure Custom Domain (Optional)

### 5.1 Frontend Domain (Vercel)

1. Go to Vercel project → **Settings** → **Domains**
2. Add your custom domain (e.g., `draftwell.com`)
3. Follow Vercel's DNS instructions

### 5.2 Backend Domain (Render)

1. Go to Render service → **Settings** → **Custom Domains**
2. Add your domain (e.g., `api.draftwell.com`)
3. Update DNS records as instructed

---

## Step 6: Test the Deployment

### 6.1 Test Frontend

1. Visit your Vercel URL
2. Navigate to different tools
3. Try the AI Detector (should work without API key for detection)
4. Try signing in

### 6.2 Test AI Features

To test AI-powered features (Humanizer, Rewriter, etc.):

1. Ensure you have added your API key to Render environment variables
2. Try humanizing a short text
3. Check if the result appears

**If AI features don't work:**
- Verify `OPENAI_API_KEY` is set correctly in Render
- Check Render logs for errors
- Ensure you have credits in your OpenAI account

### 6.3 Test Document Saving

1. Sign in with email/password
2. Generate some text
3. Click "Save"
4. Go to Workspace
5. Verify the document appears

---

## Step 7: Monitor and Maintain

### 7.1 Monitor Backend (Render)

- Go to Render dashboard
- View **Logs** for errors
- Check **Metrics** for performance
- Monitor CPU/memory usage

### 7.2 Monitor Frontend (Vercel)

- Go to Vercel dashboard
- View **Deployments** history
- Check **Analytics** (if enabled)
- Monitor bandwidth

### 7.3 Update Application

To make changes:

1. Update code locally
2. Test locally
3. Commit and push to GitHub
4. Render and Vercel will auto-deploy on push

---

## Troubleshooting

### Issue: Frontend can't connect to backend

**Solution:**
1. Verify `VITE_API_URL` is correct in Vercel
2. Check `CORS_ORIGINS` includes your Vercel domain in Render
3. Ensure backend is running (check Render logs)

### Issue: AI features return errors

**Solution:**
1. Verify API key is set in Render environment variables
2. Check you have credits in your AI provider account
3. Look at Render logs for specific error messages

### Issue: Database connection fails

**Solution:**
1. Verify `DATABASE_URL` format is correct
2. For Neon: ensure SSL mode is enabled (`sslmode=require`)
3. Check Neon dashboard for connection issues

### Issue: Build fails on Vercel

**Solution:**
1. Check Vercel build logs
2. Ensure `package.json` has correct scripts
3. Verify all dependencies are in `package.json`

### Issue: Rate limiting errors

**Solution:**
1. Increase `RATE_LIMIT_WRITES` in Render environment
2. Increase `RATE_LIMIT_WINDOW_SECONDS`
3. These are abuse protection, not paid quotas

---

## Cost Summary

### Free Tier (Testing/Development)

- **Render**: Free (spins down after 15 min inactivity)
- **Vercel**: Free (Hobby plan)
- **Neon**: Free (0.5 GB storage, limited compute)
- **AI Provider**: Pay per usage (OpenAI: ~$0.15 per 1M tokens with gpt-4o-mini)

### Production (Recommended)

- **Render**: ~$7/month (Standard Web Service)
- **Vercel**: ~$20/month (Pro plan) or free Hobby plan for personal use
- **Neon**: ~$19/month (Starter plan) or free tier for small projects
- **AI Provider**: Varies by usage (typically $5-50/month depending on traffic)

---

## Security Checklist

Before going to production:

- [ ] Changed `SECRET_KEY` to a strong random value
- [ ] All API keys are in environment variables (not in code)
- [ ] HTTPS is enabled (automatic on Vercel/Render)
- [ ] CORS origins are set correctly
- [ ] Rate limiting is configured
- [ ] Database credentials are secure
- [ ] No sensitive data in git repository

---

## Next Steps

1. **Set up monitoring**: Consider integrating error tracking (Sentry)
2. **Add analytics**: Vercel Analytics or Google Analytics
3. **Configure backups**: Neon provides automatic backups
4. **Set up CI/CD**: GitHub Actions for automated testing
5. **Custom domain**: Purchase and configure your domain

---

## Quick Reference

**Frontend URL**: https://your-app.vercel.app
**Backend URL**: https://your-api.onrender.com
**API Docs**: https://your-api.onrender.com/docs
**Render Dashboard**: https://dashboard.render.com
**Vercel Dashboard**: https://vercel.com/dashboard

---

## Support

If you encounter issues:

1. Check Render logs for backend errors
2. Check Vercel logs for frontend errors
3. Review this guide's troubleshooting section
4. Check the README.md for local development tips
5. Review ARCHITECTURE.md for system design details
