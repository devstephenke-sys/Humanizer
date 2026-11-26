# Deployment Guide

This guide covers deploying Draftwell to production using Vercel (frontend), Render (backend), and Neon (database).

## Prerequisites

- GitHub account
- Vercel account
- Render account
- Neon account (or use SQLite for simple deployments)
- AI provider API key (OpenAI, Anthropic, or Ollama)

## 1. Database Setup (Neon PostgreSQL)

### Option A: Neon (Recommended for Production)

1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string (use the pooled connection string)
4. Save the connection string for environment variables

### Option B: SQLite (Development/Small Deployments)

For simple deployments, you can use SQLite. The database file will be stored in the application directory.

## 2. Backend Deployment (Render)

### Step 1: Prepare GitHub Repository

1. Push your code to GitHub
2. Ensure the `backend/` directory is at the root level (or adjust paths accordingly)

### Step 2: Create Render Service

1. Go to https://dashboard.render.com
2. Click "New +"
3. Select "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: draftwell-api
   - **Region**: Choose closest to your users
   - **Branch**: main
   - **Root Directory**: backend
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables

Add the following environment variables in Render:

```env
ENVIRONMENT=production
SECRET_KEY=your-long-random-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
CORS_ORIGINS=https://your-frontend-domain.vercel.app
AI_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
MAX_INPUT_CHARS=60000
RATE_LIMIT_WRITES=40
RATE_LIMIT_WINDOW_SECONDS=600
```

### Step 4: Deploy

Click "Create Web Service" and wait for deployment. Render will provide a URL like `https://draftwell-api.onrender.com`

### Step 5: Run Migrations

After deployment, you may need to run database migrations. You can do this via Render's shell or by adding a pre-start script.

## 3. Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Build Frontend

```bash
cd frontend
npm run build
```

### Step 3: Deploy

```bash
cd frontend
vercel
```

Follow the prompts:
- Set project name: `draftwell`
- Build command: `npm run build`
- Output directory: `dist`
- Override directory: Leave blank

### Step 4: Configure Environment Variables

In Vercel dashboard, add:
```env
VITE_API_URL=https://your-backend-url.onrender.com
```

### Step 5: Production Build

```bash
vercel --prod
```

## 4. Alternative: Docker Deployment

### Backend Dockerfile

A Dockerfile is already included in the `backend/` directory. To build and run:

```bash
cd backend
docker build -t draftwell-api .
docker run -p 8000:8000 --env-file ../.env draftwell-api
```

### Docker Compose

Create a `docker-compose.yml` in the project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: draftwell
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: draftwell
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

## 5. Domain Configuration

### Custom Domain for Frontend (Vercel)

1. Go to Vercel project settings
2. Add your custom domain
3. Configure DNS records as instructed by Vercel

### Custom Domain for Backend (Render)

1. Go to Render service settings
2. Add custom domain
3. Configure DNS records:
   - A record pointing to Render's IP
   - Or CNAME to Render's hostname

## 6. SSL/HTTPS

- Vercel automatically provides SSL
- Render automatically provides SSL
- No additional configuration needed

## 7. Monitoring

### Backend (Render)

- Render provides built-in metrics and logs
- Access logs via Render dashboard

### Frontend (Vercel)

- Vercel Analytics (optional)
- Vercel Logs
- Consider integrating with error tracking (Sentry, etc.)

## 8. Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Configure CORS origins correctly
- [ ] Set appropriate rate limits
- [ ] Monitor logs for abuse
- [ ] Keep dependencies updated

## 9. Scaling

### Horizontal Scaling

- Render automatically scales based on demand
- Consider using a load balancer for high traffic
- Use Neon's connection pooling for database

### Database Optimization

- Use Neon's serverless PostgreSQL for auto-scaling
- Add database indexes if needed
- Monitor query performance

## 10. Troubleshooting

### Backend Won't Start

- Check environment variables are set correctly
- Verify database connection string
- Check Render logs for errors

### Frontend Can't Connect to Backend

- Verify `VITE_API_URL` is correct
- Check CORS origins in backend
- Ensure backend is running and accessible

### Database Connection Issues

- Verify database is running
- Check connection string format
- Ensure SSL mode is correct for PostgreSQL

### Rate Limiting Issues

- Adjust `RATE_LIMIT_WRITES` in environment variables
- Consider increasing window size for legitimate traffic
- Monitor for abuse patterns

## 11. Cost Estimate

### Free Tier Usage

- **Render**: Free tier available (spins down after inactivity)
- **Vercel**: Free tier available ( Hobby plan)
- **Neon**: Free tier available (0.5 GB storage)
- **AI Provider**: Depends on usage (OpenAI, Anthropic, etc.)

### Estimated Costs (Paid Tiers)

- **Render**: ~$7/month for basic web service
- **Vercel**: ~$20/month for Pro plan
- **Neon**: ~$19/month for starter plan
- **AI Provider**: Varies by provider and usage

## 12. Backup Strategy

### Database Backup

- Neon provides automated backups
- Export regular dumps: `pg_dump`
- Store backups in secure location

### Code Backup

- Code is in GitHub
- Tag releases for version control
- Maintain feature branches

## 13. Rollback Procedure

### Backend Rollback

1. Go to Render dashboard
2. View deploy history
3. Click on previous successful deployment
4. Redeploy that commit

### Frontend Rollback

1. Go to Vercel dashboard
2. View deployments
3. Promote previous deployment to production

## 14. Update Procedure

1. Test changes in development
2. Create a pull request
3. Review and merge to main
4. Trigger deployments (automatic on push)
5. Monitor logs and metrics
6. Roll back if issues occur
