# TrumpCoin Benefit Program

A Django-based web application for managing the TrumpCoin Benefit program, allowing users to apply for benefits and administrators to manage applications.

## Features

- User registration and authentication
- Two-step application process
- Application status tracking
- Admin dashboard for application management
- Secure handling of user data
- Email notifications

## Technology Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (can be configured for PostgreSQL)
- **Authentication**: Django Authentication System

## Project Structure

- `benefit/`: Main Django app
  - `models.py`: Database models
  - `views.py`: User-facing views
  - `admin_views.py`: Admin dashboard views
  - `forms.py`: Form definitions
  - `urls.py`: URL routing
  - `templatetags/`: Custom template tags
- `templates/benefit/`: HTML templates
  - `admin/`: Admin dashboard templates
- `static/benefit/`: Static files
  - `css/`: CSS stylesheets
  - `js/`: JavaScript files
  - `img/`: Images

## Development Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/trumpcoin-benefit.git
   cd trumpcoin-benefit
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows using Command Prompt:
   venv\Scripts\activate.bat
   
   # On Windows using PowerShell (if allowed):
   # .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux:
   # source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://localhost:8000

## Admin Access

To access the admin dashboard:

1. Log in with a superuser account
2. Navigate to http://localhost:8000/admin-dashboard/

## Deployment Guide

This guide provides step-by-step instructions for deploying the TrumpCoin Benefit Program to different platforms.

### Option 1: Deploy to Render.com (Recommended for Beginners)

Render.com offers a free tier that includes PostgreSQL databases and custom domain support, making it perfect for deploying your TrumpCoin Benefit application.

#### Step 1: Prepare Your Project for Render

1. **Create a `render.yaml` file** in your project root:

```yaml
services:
  - type: web
    name: trumpcoin-benefit
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn trumpcoin_benefit.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: WEB_CONCURRENCY
        value: 4
      - key: DJANGO_SETTINGS_MODULE
        value: trumpcoin_benefit.render_settings
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: trumpcoin-db
          property: connectionString

databases:
  - name: trumpcoin-db
    databaseName: trumpcoin
    user: trumpcoin_user
```

2. **Create a `trumpcoin_benefit/render_settings.py` file**:

```python
import os
import dj_database_url
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['trumpcoin-benefit.onrender.com', 'trumpcoin-benefit.live', 'www.trumpcoin-benefit.live']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Simplified static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise middleware
    # ... rest of your middleware
] + MIDDLEWARE

# Email configuration (using Zoho Mail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('ZOHO_EMAIL_USER', '')  # your full Zoho email address
EMAIL_HOST_PASSWORD = os.environ.get('ZOHO_EMAIL_PASSWORD', '')  # your Zoho email password or app password
DEFAULT_FROM_EMAIL = 'TrumpCoin Benefit <noreply@trumpcoin-benefit.live>'

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

3. **Update your `requirements.txt` file** to include these packages:

```
dj-database-url==2.1.0
whitenoise==6.4.0
gunicorn==21.2.0
psycopg2-binary==2.9.6
```

#### Step 2: Create a Render Account and Deploy

1. **Sign up for Render**:
   - Go to [render.com](https://render.com/) and sign up for a free account

2. **Connect your GitHub repository**:
   - In the Render dashboard, click "New" and select "Blueprint"
   - Connect your GitHub account and select your repository
   - If you don't have your code on GitHub, you can also deploy directly from your local machine

3. **Configure your service**:
   - Render will automatically detect your `render.yaml` file
   - Review the settings and click "Apply"

4. **Wait for deployment**:
   - Render will build and deploy your application
   - This may take a few minutes

5. **Set up your database**:
   - Render will automatically create a PostgreSQL database based on your `render.yaml` file

6. **Run migrations**:
   - Once deployed, go to the "Shell" tab in your web service
   - Run: `python manage.py migrate`
   - Run: `python manage.py createsuperuser` and follow the prompts

#### Step 3: Set Up Your Custom Domain (trumpcoin-benefit.live)

1. **Add your domain in Render**:
   - Go to your web service in Render
   - Click on "Settings" and scroll to "Custom Domain"
   - Click "Add Custom Domain" and enter: `trumpcoin-benefit.live`
   - Also add: `www.trumpcoin-benefit.live`

2. **Configure DNS settings**:
   - Render will provide you with DNS records to add to your domain registrar
   - Log in to your domain registrar (where you purchased trumpcoin-benefit.live)
   - Add the CNAME records provided by Render:
     - `trumpcoin-benefit.live` → `[your-app-name].onrender.com`
     - `www.trumpcoin-benefit.live` → `[your-app-name].onrender.com`

3. **Verify and secure your domain**:
   - Render will automatically provision a free SSL certificate for your domain
   - Wait for DNS propagation (can take up to 48 hours, but usually much faster)

#### Step 4: Set Up Email (SendGrid Example)

1. **Create a SendGrid account**:
   - Go to [sendgrid.com](https://sendgrid.com/) and sign up for a free account
   - Verify your account and create an API key

2. **Add the API key to Render**:
   - Go to your web service in Render
   - Click on "Environment" and add a new environment variable:
     - Key: `SENDGRID_API_KEY`
     - Value: Your SendGrid API key
   - Click "Save Changes" and wait for your service to redeploy

## Deploying to Koyeb with Zoho Email - Step by Step Guide

This guide will walk you through deploying your TrumpCoin Benefit application to Koyeb with Zoho for email sending.

### Files You Need to Modify Before Deployment

1. **`trumpcoin_benefit/koyeb_settings.py`**
   - Already created for you, but review the following settings:
   - `SECRET_KEY`: Will be set via environment variable
   - `ALLOWED_HOSTS`: Update if your domain is different from trumpcoin-benefit.live
   - Email settings: Will be updated for Zoho

2. **`.python-version`**
   - Already created with Python 3.9 specified
   - This file tells Koyeb which Python version to use
   - **IMPORTANT**: Do not remove this file or deployment will fail

3. **`.gitignore`**
   - Already set up correctly, no changes needed

4. **`Procfile`**
   - Already created, no changes needed

5. **`requirements.txt`**
   - Already updated with all necessary dependencies
   - Uses compatible versions of Django (4.2.7) and Pillow (9.5.0)
   - **IMPORTANT**: Do not upgrade these packages without testing, as newer versions may cause deployment issues

### Step 1: Generate a Secure Secret Key

1. Run this command in your terminal to generate a secure secret key:
   ```
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
2. Copy the output - you'll need this for your Koyeb environment variables

### Step 2: Set Up Zoho Email for Your Domain

1. **Create a Zoho Mail account**:
   - Go to [zoho.com/mail](https://www.zoho.com/mail/) and sign up for a free account
   - Choose the Free plan (up to 5 users, 5GB/user)

2. **Add your domain (trumpcoin-benefit.live)**:
   - In Zoho Mail admin panel, go to "Domain" > "Add Domain"
   - Enter your domain: `trumpcoin-benefit.live`
   - Follow the verification process (usually adding TXT or CNAME records to your domain)

3. **Create an email address**:
   - Create `noreply@trumpcoin-benefit.live` or similar
   - Set a strong password

4. **Generate an App Password for SMTP**:
   - Go to "My Account" > "Security" > "App Passwords"
   - Click "Generate New Password"
   - Name it "TrumpCoin Benefit App"
   - Copy the generated password - you'll need this for Koyeb environment variables

### Step 3: Push Your Code to GitHub

Follow the GitHub repository setup guide in the previous section, or if you've already done that, make sure your repository is up to date:

```
git add .
git commit -m "Prepare for Koyeb deployment"
git push
```

### Step 4: Create a Koyeb Account and Deploy

1. **Sign up for Koyeb**:
   - Go to [koyeb.com](https://koyeb.com/) and sign up for a free account
   - Verify your email address

2. **Create a new app**:
   - Click "Create App"
   - Select "GitHub" as the deployment method
   - Connect your GitHub account when prompted
   - Select your `trumpcoin-benefit` repository
   - Configure the build:
     - Name: `trumpcoin-benefit`
     - Region: Choose the closest to your users
     - Instance Type: Nano (free tier)
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn trumpcoin_benefit.wsgi:application`

3. **Add environment variables**:
   - Click on "Environment" tab and add these variables:
     - `DJANGO_SETTINGS_MODULE`: `trumpcoin_benefit.koyeb_settings`
     - `SECRET_KEY`: Paste the secret key you generated in Step 1
     - `PORT`: `8000`  # Koyeb will use this for the health check
     - `EMAIL_HOST`: `smtp.zoho.com`
     - `EMAIL_PORT`: `587`
     - `EMAIL_HOST_USER`: `noreply@trumpcoin-benefit.live` (or your Zoho email)
     - `EMAIL_HOST_PASSWORD`: Your Zoho app password from Step 2

4. **Add a database**:
   - In the Koyeb dashboard, go to "Database" and click "Create Database"
   - Select PostgreSQL and the free tier
   - Name it `trumpcoin-db`
   - Once created, get the connection string from the database details page
   - Add it as an environment variable in your app:
     - `DATABASE_URL`: Your PostgreSQL connection string

5. **Deploy your app**:
   - Click "Deploy" and wait for the deployment to complete
   - This may take a few minutes

### Step 5: Run Migrations and Create Superuser

1. **Access the web terminal**:
   - Go to your app in Koyeb dashboard
   - Click on "Web Terminal" tab

2. **Run migrations**:
   ```
   python manage.py migrate
   ```

3. **Create a superuser**:
   ```
   python manage.py createsuperuser
   ```
   - Follow the prompts to create an admin account

4. **Collect static files**:
   ```
   python manage.py collectstatic --noinput
   ```

### Step 6: Set Up Your Custom Domain (trumpcoin-benefit.live)

1. **Add your domain in Koyeb**:
   - Go to your app in Koyeb
   - Click on "Settings" > "Domains"
   - Click "Add Domain" and enter: `trumpcoin-benefit.live`
   - Also add: `www.trumpcoin-benefit.live`

2. **Configure DNS settings**:
   - Koyeb will provide you with DNS records to add to your domain registrar
   - Log in to your domain registrar (where you purchased trumpcoin-benefit.live)
   - Add the CNAME records provided by Koyeb:
     - `trumpcoin-benefit.live` → The Koyeb domain provided
     - `www.trumpcoin-benefit.live` → The Koyeb domain provided

3. **Verify and secure your domain**:
   - Koyeb will automatically provision a free SSL certificate for your domain
   - Wait for DNS propagation (can take up to 48 hours, but usually much faster)

### Step 7: Update Email Settings (If Needed)

If you need to update your email settings after deployment:

1. Go to your app in Koyeb dashboard
2. Click on "Environment" tab
3. Update the email-related environment variables
4. Save changes and wait for redeployment

### Step 8: Test Your Deployment

1. Visit your domain: `https://trumpcoin-benefit.live`
2. Test user registration to verify email sending
3. Log in to the admin dashboard: `https://trumpcoin-benefit.live/admin-dashboard/`
4. Test the application functionality

### Troubleshooting Koyeb Deployment

1. **Application not starting or health check failing**:
   - Check the logs in Koyeb dashboard
   - Verify your environment variables are set correctly, especially the `PORT` variable
   - Make sure the Procfile is correctly configured with `--bind 0.0.0.0:$PORT`
   - Ensure your application is listening on the port specified in the environment variable
   - Make sure your `requirements.txt` includes all dependencies

2. **Database connection issues**:
   - Verify the `DATABASE_URL` environment variable is correct
   - Check if your database service is running in Koyeb

3. **Static files not loading**:
   - Run `python manage.py collectstatic --noinput` in the web terminal
   - Check if WhiteNoise is configured correctly

4. **Email not sending**:
   - Verify your Zoho credentials
   - Check if your Zoho account is properly set up
   - Look for error messages in the logs

5. **Custom domain not working**:
   - Verify DNS settings at your domain registrar
   - Check if SSL certificate has been provisioned
   - Allow time for DNS propagation

### Maintenance and Updates

To update your application after making changes:

1. Push changes to GitHub:
   ```
   git add .
   git commit -m "Description of changes"
   git push
   ```

2. Koyeb will automatically detect changes and redeploy your application

3. If you need to run migrations after an update:
   - Access the web terminal in Koyeb
   - Run: `python manage.py migrate`

## Common Deployment Tasks

Regardless of which platform you choose, here are some common tasks you'll need to perform:

### Setting Up Email

For both platforms, you can use various email providers:

1. **SendGrid** (recommended for beginners):
   - Free tier includes 100 emails/day
   - Simple API and SMTP integration
   - Good deliverability

2. **Gmail** (for testing):
   - Enable 2-Step Verification
   - Generate an App Password
   - Use in your settings:
     ```
     EMAIL_HOST = 'smtp.gmail.com'
     EMAIL_PORT = 587
     EMAIL_USE_TLS = True
     EMAIL_HOST_USER = 'your-email@gmail.com'
     EMAIL_HOST_PASSWORD = 'your-app-password'
     ```

### Managing Static Files

Both Render and Koyeb can serve static files using WhiteNoise:

1. Make sure WhiteNoise is in your `requirements.txt`
2. Add WhiteNoise to your middleware in settings
3. Set `STATIC_ROOT` and `STATICFILES_STORAGE` as shown in the example settings
4. Run `python manage.py collectstatic` before deploying

### Database Backups

For both platforms, you can set up regular database backups:

1. **Render**:
   - PostgreSQL databases on Render have automatic daily backups
   - You can also create manual backups from the dashboard

2. **Koyeb**:
   - Use a scheduled task to run `pg_dump` and store the backup
   - Or use a third-party service like pgBackRest

### Monitoring Your Application

Both platforms provide basic monitoring:

1. **Render**:
   - View logs in the "Logs" tab
   - Set up alerts for service health

2. **Koyeb**:
   - View logs in the "Logs" section
   - Monitor resource usage in the dashboard

## GitHub Repository Setup for Deployment

To deploy your TrumpCoin Benefit application to platforms like Render.com or Koyeb, you'll need to push your code to a GitHub repository. Here's a step-by-step guide for beginners:

### Step 1: Create a GitHub Account

1. Go to [github.com](https://github.com/) and sign up for a free account if you don't already have one
2. Verify your email address

### Step 2: Install Git on Your Computer

1. **Windows**:
   - Download Git from [git-scm.com](https://git-scm.com/download/win)
   - Run the installer with default options
   - Open Command Prompt or Git Bash to verify installation: `git --version`

2. **macOS**:
   - If you have Homebrew: `brew install git`
   - Otherwise, download from [git-scm.com](https://git-scm.com/download/mac)
   - Open Terminal to verify installation: `git --version`

3. **Linux (Ubuntu/Debian)**:
   - `sudo apt update`
   - `sudo apt install git`
   - Verify installation: `git --version`

### Step 3: Configure Git

1. Open Command Prompt/Terminal and set your identity:
   ```
   git config --global user.name "trumpcoin-benefit"
   git config --global user.email "admin@trumpcoin-benefit.live"
   ```

### Step 4: Create a New GitHub Repository

1. Log in to GitHub
2. Click the "+" icon in the top-right corner and select "New repository"
3. Repository name: `trumpcoin-benefit`
4. Description: `TrumpCoin Benefit Program - Django Application`
5. Choose "Private" if you want to keep your code private, or "Public" if you want it to be visible to everyone
6. Do NOT initialize with README, .gitignore, or license (we'll push our existing project)
7. Click "Create repository"

### Step 5: Initialize Git in Your Project

1. Open Command Prompt/Terminal
2. Navigate to your project directory:
   ```
   cd path/to/trumpcoin-benefit
   ```
3. Initialize Git repository:
   ```
   git init
   ```

### Step 6: Add Your Files to Git

1. Add all files to staging:
   ```
   git add .
   ```
2. Commit the files:
   ```
   git commit -m "Initial commit"
   ```

### Step 7: Connect to GitHub and Push

1. Connect your local repository to GitHub (replace `yourusername` with your GitHub username):
   ```
   git remote add origin https://github.com/yourusername/trumpcoin-benefit.git
   ```
2. Push your code to GitHub:
   ```
   git push -u origin main
   ```
   Note: If you're using an older version of Git, you might need to use `master` instead of `main`:
   ```
   git push -u origin master
   ```
3. If prompted, enter your GitHub username and password (or personal access token)

### Step 8: Verify Your Repository

1. Go to `https://github.com/yourusername/trumpcoin-benefit`
2. You should see all your project files there

### Step 9: Update Your Code in the Future

Whenever you make changes to your code and want to update the repository:

1. Add the changed files:
   ```
   git add .
   ```
2. Commit the changes:
   ```
   git commit -m "Description of changes"
   ```
3. Push to GitHub:
   ```
   git push
   ```

### Step 10: Connect Your Repository to Deployment Platforms

1. **For Render.com**:
   - In the Render dashboard, click "New" and select "Blueprint"
   - Connect your GitHub account when prompted
   - Select your `trumpcoin-benefit` repository
   - Render will detect your `render.yaml` file and set up the services

2. **For Koyeb**:
   - In the Koyeb dashboard, click "Create App"
   - Select "GitHub" as the deployment method
   - Connect your GitHub account when prompted
   - Select your `trumpcoin-benefit` repository
   - Configure the build settings as described in the deployment guide

## Troubleshooting

### Common Issues and Solutions

1. **Application not starting**:
   - Check the logs for error messages
   - Verify your environment variables are set correctly
   - Make sure your `requirements.txt` includes all dependencies

2. **Database connection issues**:
   - Verify the `DATABASE_URL` environment variable is set correctly
   - Check if your database service is running
   - Ensure your IP is allowed to connect to the database

3. **Static files not loading**:
   - Make sure WhiteNoise is configured correctly in your settings file
   - Ensure `STATICFILES_DIRS` is properly set to include your static files directory
   - Verify that `collectstatic` is running during the build process
   - Check that the `STATIC_ROOT` directory is being properly served
   - For Render.com specifically:
     - Make sure your `render.yaml` includes `collectstatic` in the build command
     - Ensure WhiteNoise middleware is properly configured in your settings
     - Try temporarily setting `DEBUG = True` to see if that helps identify the issue
     - Use the diagnostic tools provided (see "Diagnostic Tools" section below)
   - Check the browser console for 404 errors and specific paths that are failing

## Diagnostic Tools

The application includes several diagnostic tools to help troubleshoot deployment issues:

1. **Static File Tests**:
   - `/static/test.html` - A simple HTML file to test if static files are being served
   - `/static/test-with-css.html` - Tests if external CSS files are loading correctly

2. **Django Diagnostic Views**:
   - `/debug-info/` - Displays detailed information about the environment, settings, and static files
   - `/test-template/` - Tests if Django templates are rendering correctly
   - `/test-500/` - Deliberately triggers a 500 error to test error handling

3. **Deployment Scripts**:
   - `deployment/render_deploy.sh` - Script to help deploy to Render.com
   - `deployment/render_static_files_guide.md` - Detailed guide for fixing static files issues on Render.com

To use the deployment script:

**On Linux/macOS:**
```bash
# Make the script executable (if not already)
chmod +x deployment/render_deploy.sh

# Run the script
./deployment/render_deploy.sh
```

**On Windows:**
```
# Run the Windows batch script
deployment\render_deploy.bat
```

The script will guide you through the deployment process, including collecting static files, committing changes, and pushing to GitHub.

4. **Email not sending**:
   - Verify your email provider credentials
   - Check if your email provider blocks automated emails
   - Look for error messages in the logs

5. **Custom domain not working**:
   - Verify DNS settings are correct
   - Check if SSL certificate has been provisioned
   - Allow time for DNS propagation (up to 48 hours)

6. **Git and GitHub issues**:
   - **"Permission denied" error**: Make sure you have the correct credentials or use a personal access token
   - **"Repository not found" error**: Check that the repository URL is correct
   - **"Rejected non-fast-forward" error**: Pull changes before pushing: `git pull --rebase origin main`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"# trumpcoin-benefit" 
"# trumpcoin-benefit" 
"# trumpcoin-benefit" 
#   t r u m p c o i n - b e n e f i t 
