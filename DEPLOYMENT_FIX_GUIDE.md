# Database Reset Issue - Complete Fix Guide

## The Problem
Your SQLite database was getting wiped on every Render deployment because:
1. SQLite stores data in files on the server's filesystem
2. Render completely recreates the filesystem on each deployment
3. Your PostgreSQL wasn't properly connecting, causing fallback to SQLite

## What We Fixed

### 1. Updated render.yaml
- Added `python manage.py migrate` to the build command
- This ensures PostgreSQL tables are created before the app starts

### 2. Improved create_superuser.py
- Added database connection testing
- Better error handling to catch PostgreSQL connection issues
- Will fail deployment if database isn't working (preventing SQLite fallback)

### 3. Created test_database.py
- Test script to verify database connection locally
- Helps diagnose issues before deployment

## Step-by-Step Deployment Process

### Step 1: Test Locally (Optional but Recommended)
```bash
python test_database.py
```
This will verify your PostgreSQL connection works with your current settings.

### Step 2: Deploy to Render
1. Commit your changes:
   ```bash
   git add .
   git commit -m "Fix database reset issue - add migrations to deployment"
   git push
   ```

2. Go to your Render dashboard
3. Trigger a new deployment
4. Watch the build logs carefully

### Step 3: Monitor the Build Logs
Look for these key messages:
- ✅ `pip install -r requirements.txt` - Dependencies installed
- ✅ `python manage.py migrate` - Database tables created
- ✅ `Database connection successful!` - PostgreSQL working
- ✅ `Superuser admin already exists` or `Superuser created successfully!`

### Step 4: Verify After Deployment
1. Log into your admin panel: `https://your-app.onrender.com/admin/`
2. Check that your users are still there
3. Create a test user to verify data persistence

## If PostgreSQL Still Doesn't Work

### Check These Common Issues:

1. **Database Service Status**
   - Go to Render Dashboard → Databases
   - Ensure your `trumpcoin-db` is running and healthy

2. **Environment Variables**
   - Verify `DATABASE_URL` is properly set in your web service
   - Should be automatically populated from your database

3. **Database Connection String**
   - In your render_settings.py, the DATABASE_URL should look like:
   - `postgresql://username:password@host:port/database_name`

4. **Network Connectivity**
   - Render's free tier databases sometimes have connectivity issues
   - Try restarting both your web service and database

## Alternative Solutions

### Option A: Use Render's Persistent Disk (Not Recommended)
If PostgreSQL absolutely won't work, you could use persistent disk for SQLite:
- Add a persistent disk to your Render service
- Store SQLite database on the persistent disk
- **Warning**: This is not recommended for production

### Option B: Switch to Another Database Provider
- Use Railway, Supabase, or Neon for PostgreSQL
- Update your DATABASE_URL environment variable

### Option C: Use Render's Managed PostgreSQL
- Ensure you're using Render's own PostgreSQL service
- Check the connection string format

## Testing Your Fix

After deployment, test these scenarios:
1. Create a new user account
2. Deploy again (trigger manual deployment)
3. Verify the user account still exists
4. Check admin panel for all previous data

## Troubleshooting Commands

If you need to debug on Render:

1. **Check Database Connection**:
   Add this to your build command temporarily:
   ```bash
   python test_database.py
   ```

2. **Manual Migration**:
   If migrations fail, you can run them manually in Render's shell

3. **Reset Database** (Last Resort):
   If you need to start fresh:
   - Delete and recreate your database in Render
   - Redeploy your application

## Success Indicators

✅ **Your fix worked if:**
- Build logs show successful database connection
- Migrations run without errors
- Users persist between deployments
- No more "database reset" issues

❌ **Still having issues if:**
- Build fails during migration step
- Users disappear after deployment
- Getting database connection errors

## Need Help?

If you're still having issues:
1. Share the build logs from Render
2. Check your database service status
3. Verify environment variables are set correctly
4. Consider switching database providers if Render's PostgreSQL continues to have issues

Remember: The key is ensuring PostgreSQL connects properly during deployment. If it fails, Django falls back to SQLite, which gets wiped on every deployment.
