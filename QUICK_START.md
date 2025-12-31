# Quick Start: Deploy to Vercel

## TL;DR - Fast Deployment

### 1. Deploy Backend (FastAPI)

```bash
cd backend
vercel --prod
```

**Set these environment variables in Vercel Dashboard:**
- `SUPABASE_URL` - Your Supabase URL
- `SUPABASE_KEY` - Your Supabase key

**Save the deployment URL** (e.g., `https://your-backend.vercel.app`)

### 2. Deploy Frontend (Next.js)

```bash
cd frontend
vercel --prod
```

**Set this environment variable in Vercel Dashboard:**
- `NEXT_PUBLIC_API_URL` - Your backend URL from step 1

**Redeploy** after adding the environment variable.

### 3. Update CORS (if needed)

Edit `backend/app/main.py` and add your frontend URL to `allow_origins`:

```python
allow_origins=[
    "https://your-frontend.vercel.app",
    "http://localhost:3000",
],
```

Then redeploy the backend.

## Using Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository
3. For backend: Set **Root Directory** to `backend`
4. For frontend: Set **Root Directory** to `frontend`
5. Add environment variables as listed above

## Important Notes

⚠️ **File Storage**: The backend uses `/tmp` in serverless (ephemeral). Files are deleted after function execution. Consider using cloud storage for production.

⚠️ **Timeouts**: Large file processing may timeout. Consider async processing or background jobs.

See `DEPLOYMENT.md` for detailed instructions and troubleshooting.

