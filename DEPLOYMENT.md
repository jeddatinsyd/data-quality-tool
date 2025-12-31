# Vercel Deployment Guide

This guide will help you deploy both your Next.js frontend and FastAPI backend to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Vercel CLI installed (optional, but recommended):
   ```bash
   npm i -g vercel
   ```

## Project Structure

- `/frontend` - Next.js application
- `/backend` - FastAPI Python application

## Deployment Steps

### Step 1: Deploy Backend (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Login to Vercel (if using CLI):**
   ```bash
   vercel login
   ```

3. **Deploy the backend:**
   ```bash
   vercel
   ```
   
   Or deploy via Vercel Dashboard:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - Set the **Root Directory** to `backend`
   - Vercel will auto-detect Python

4. **Set Environment Variables:**
   
   In Vercel Dashboard → Your Project → Settings → Environment Variables, add:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase API key
   - `PYTHON_VERSION` - `3.11` (or your preferred version)

5. **Note the Backend URL:**
   
   After deployment, Vercel will provide a URL like:
   `https://your-backend-project.vercel.app`
   
   **Save this URL** - you'll need it for the frontend configuration.

### Step 2: Deploy Frontend (Next.js)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Deploy the frontend:**
   ```bash
   vercel
   ```
   
   Or deploy via Vercel Dashboard:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - Set the **Root Directory** to `frontend`
   - Vercel will auto-detect Next.js

3. **Set Environment Variables:**
   
   In Vercel Dashboard → Your Project → Settings → Environment Variables, add:
   - `NEXT_PUBLIC_API_URL` - Your backend URL from Step 1 (e.g., `https://your-backend-project.vercel.app`)
   
   **Important:** The `NEXT_PUBLIC_` prefix makes this variable available in the browser.

4. **Redeploy:**
   
   After adding environment variables, trigger a new deployment:
   - Go to Deployments tab
   - Click "..." on the latest deployment
   - Select "Redeploy"

### Step 3: Update CORS Settings (Backend)

After deploying both apps, you may need to update CORS settings in your backend:

1. **Edit `backend/app/main.py`:**
   
   Update the `allow_origins` to include your frontend URL:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://your-frontend-project.vercel.app",
           "http://localhost:3000",  # Keep for local development
       ],
       allow_credentials=False,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Redeploy the backend** after making this change.

## Alternative: Using Vercel CLI for Both Projects

If you prefer using the CLI:

### Backend:
```bash
cd backend
vercel --prod
```

### Frontend:
```bash
cd frontend
vercel --prod
```

## Environment Variables Summary

### Backend Environment Variables:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase API key
- `PYTHON_VERSION` - Python version (default: 3.11)

### Frontend Environment Variables:
- `NEXT_PUBLIC_API_URL` - Backend API URL (e.g., `https://your-backend.vercel.app`)

## Important Notes

### File Storage Limitation

⚠️ **Important:** Your backend currently uses local file storage (`temp_uploads/`). In Vercel's serverless environment:
- Files are stored in `/tmp` which is ephemeral
- Files are deleted after each function execution
- Consider using:
  - **Vercel Blob Storage** for file uploads
  - **Supabase Storage** (since you're already using Supabase)
  - **AWS S3** or similar cloud storage

### Serverless Function Timeout

Vercel serverless functions have execution time limits:
- Hobby plan: 10 seconds
- Pro plan: 60 seconds
- Enterprise: Custom limits

For large file processing, consider:
- Processing files asynchronously
- Using Vercel's background functions
- Moving heavy processing to a separate service

### Database Considerations

If you're using Supabase, ensure:
- Your Supabase project allows connections from Vercel's IP ranges
- Database connection pooling is configured properly
- Environment variables are set correctly

## Troubleshooting

### Backend Issues

1. **Import errors:**
   - Ensure `api/index.py` correctly references your app
   - Check that all dependencies are in `requirements.txt`

2. **Function timeout:**
   - Optimize file processing
   - Consider chunking large files
   - Use background jobs for heavy processing

3. **CORS errors:**
   - Verify frontend URL is in `allow_origins`
   - Check that environment variables are set correctly

### Frontend Issues

1. **API connection errors:**
   - Verify `NEXT_PUBLIC_API_URL` is set correctly
   - Check that the backend URL is accessible
   - Ensure CORS is configured on the backend

2. **Build errors:**
   - Check Node.js version compatibility
   - Verify all dependencies are in `package.json`
   - Review build logs in Vercel dashboard

## Local Development

For local development, create `.env.local` files:

### `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### `backend/.env.local`:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel Next.js Documentation](https://vercel.com/docs/frameworks/nextjs)
- [FastAPI on Vercel](https://vercel.com/guides/deploying-fastapi-with-vercel)

