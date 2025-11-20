# CuraLink Deployment Guide

Complete guide for deploying CuraLink to production using various platforms.

## 📋 Prerequisites

- GitHub repository: https://github.com/astitva16-shadow/CuraLink
- Python 3.10+
- PostgreSQL database (for production)

## 🚀 Quick Deploy Options

### Option 1: Deploy to Render (Recommended)

Render offers free PostgreSQL and web hosting with automatic deployments.

#### Steps:

1. **Sign up at [Render](https://render.com)**
   - Connect your GitHub account

2. **Create a PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `curalink-db`
   - Plan: Free
   - Note the Internal Database URL

3. **Create a Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository: `astitva16-shadow/CuraLink`
   - Settings:
     - Name: `curalink`
     - Environment: `Python 3`
     - Build Command: `chmod +x build.sh && ./build.sh`
     - Start Command: `gunicorn curalink.wsgi:application`
     - Plan: Free

4. **Set Environment Variables**
   ```
   SECRET_KEY=your-super-secret-key-here-change-this
   DEBUG=False
   ALLOWED_HOSTS=curalink.onrender.com
   DATABASE_URL=<paste-internal-database-url-from-step-2>
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_PASSWORD=your-admin-password
   DJANGO_SUPERUSER_EMAIL=admin@curalink.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Your app will be live at `https://curalink.onrender.com`

---

### Option 2: Deploy to Railway

Railway offers $5 free credit monthly with PostgreSQL included.

#### Steps:

1. **Sign up at [Railway](https://railway.app)**
   - Connect GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `astitva16-shadow/CuraLink`

3. **Add PostgreSQL**
   - Click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway auto-creates DATABASE_URL

4. **Configure Web Service**
   - Settings → Environment Variables:
     ```
     SECRET_KEY=your-super-secret-key-here-change-this
     DEBUG=False
     ALLOWED_HOSTS=${{RAILWAY_STATIC_URL}}
     DJANGO_SUPERUSER_USERNAME=admin
     DJANGO_SUPERUSER_PASSWORD=your-admin-password
     DJANGO_SUPERUSER_EMAIL=admin@curalink.com
     ```
   - Settings → Build Command: `chmod +x build.sh && ./build.sh`
   - Settings → Start Command: `gunicorn curalink.wsgi:application`

5. **Deploy**
   - Railway auto-deploys on push
   - Access at generated Railway URL

---

### Option 3: Deploy to PythonAnywhere

PythonAnywhere offers free hosting with manual setup.

#### Steps:

1. **Sign up at [PythonAnywhere](https://www.pythonanywhere.com)**
   - Free tier: `yourusername.pythonanywhere.com`

2. **Clone Repository**
   ```bash
   cd ~
   git clone https://github.com/astitva16-shadow/CuraLink.git
   cd CuraLink
   ```

3. **Create Virtual Environment**
   ```bash
   mkvirtualenv curalink --python=/usr/bin/python3.10
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Use SQLite for free tier (already configured)
   - Or upgrade for MySQL/PostgreSQL

5. **Set Environment Variables**
   - Create `.env` file:
     ```
     SECRET_KEY=your-super-secret-key-here
     DEBUG=False
     ALLOWED_HOSTS=yourusername.pythonanywhere.com
     ```

6. **Setup Web App**
   - Web → Add New Web App → Manual Configuration → Python 3.10
   - Source code: `/home/yourusername/CuraLink`
   - Virtualenv: `/home/yourusername/.virtualenvs/curalink`
   - WSGI file: Point to `/home/yourusername/CuraLink/curalink/wsgi.py`

7. **Static Files**
   - Run: `python manage.py collectstatic`
   - In Web tab, set static URL: `/static/`
   - Set static directory: `/home/yourusername/CuraLink/staticfiles/`

8. **Initialize Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py import_hospitals
   ```

9. **Reload**
   - Click "Reload" button in Web tab

---

### Option 4: Deploy to Heroku

Heroku offers free dyno hours (requires credit card verification).

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   cd CuraLink
   heroku create curalink-app
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-super-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set DJANGO_SUPERUSER_USERNAME=admin
   heroku config:set DJANGO_SUPERUSER_PASSWORD=your-admin-password
   heroku config:set DJANGO_SUPERUSER_EMAIL=admin@curalink.com
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Initialize Database**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py import_hospitals
   ```

7. **Open App**
   ```bash
   heroku open
   ```

---

## 🔑 Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (generate a secure random string) | `django-insecure-xyz123...` |
| `DEBUG` | Debug mode (always False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `curalink.onrender.com,www.curalink.com` |
| `DATABASE_URL` | PostgreSQL connection string (auto-set by platform) | `postgresql://user:pass@host:5432/db` |
| `DJANGO_SUPERUSER_USERNAME` | Admin username (for auto-creation) | `admin` |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password (for auto-creation) | `SecurePassword123!` |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | `admin@curalink.com` |

### Generate a Secure SECRET_KEY

```python
# Run this in Python shell
import secrets
print(secrets.token_urlsafe(50))
```

---

## 📦 Post-Deployment Steps

### 1. Access Admin Panel
- Navigate to `https://your-domain.com/admin/`
- Login with superuser credentials
- Verify hospital data is imported

### 2. Test PWA Features
- Open app on mobile device
- Click "Install App" prompt
- Test offline functionality
- Verify GPS location access

### 3. Verify Deployment
- Homepage loads correctly
- Dark mode toggle works
- Hospital finder shows real data
- Map displays with markers
- Appointment booking functional

### 4. Monitor Logs
```bash
# Render
render logs --app curalink

# Railway
railway logs

# Heroku
heroku logs --tail
```

---

## 🛠️ Troubleshooting

### Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic --no-input
```

### Database Connection Error

**Solution:**
- Verify DATABASE_URL is set correctly
- Check PostgreSQL service is running
- Ensure database migrations ran: `python manage.py migrate`

### 500 Internal Server Error

**Solution:**
- Check logs for detailed error
- Verify all environment variables are set
- Ensure DEBUG=False and ALLOWED_HOSTS includes your domain

### WhiteNoise Static Files Warning

**Solution:**
- Run `collectstatic` before deployment
- Verify `STATICFILES_STORAGE` setting in settings.py

### Hospital Data Not Showing

**Solution:**
```bash
python manage.py import_hospitals
```

---

## 🔄 Updating Your Deployment

### For Render/Railway (Auto-Deploy)
```bash
git add .
git commit -m "Update feature"
git push origin main
# Platform auto-deploys
```

### For PythonAnywhere (Manual)
```bash
cd ~/CuraLink
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
# Click "Reload" in Web tab
```

### For Heroku
```bash
git add .
git commit -m "Update feature"
git push heroku main
```

---

## 🌐 Custom Domain Setup

### Render
1. Go to Settings → Custom Domains
2. Add your domain (e.g., `curalink.com`)
3. Update DNS with provided CNAME record
4. Update `ALLOWED_HOSTS` in environment variables

### Railway
1. Settings → Domains → Add Custom Domain
2. Follow DNS instructions
3. Update `ALLOWED_HOSTS`

### PythonAnywhere
1. Upgrade to paid account
2. Web → Add custom domain
3. Follow DNS setup instructions

---

## 📊 Performance Optimization

### Enable Caching
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'curalink_cache',
    }
}
```

### Database Indexing
- Already optimized in models
- Run `python manage.py migrate` to apply

### CDN for Static Files
- Use Cloudflare for free CDN
- Configure STATIC_URL to CDN endpoint

---

## 📞 Support

- **Documentation**: See other guides in repository
- **Issues**: https://github.com/astitva16-shadow/CuraLink/issues
- **PWA Setup**: See PWA_SETUP_GUIDE.md
- **Features**: See FEATURES_LIST.md

---

## ✅ Deployment Checklist

- [ ] Database created and connected
- [ ] Environment variables configured
- [ ] SECRET_KEY generated and set
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Static files collected
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Hospital data imported
- [ ] HTTPS/SSL enabled
- [ ] Custom domain configured (optional)
- [ ] PWA features tested
- [ ] Backup strategy implemented

---

**Deployment completed! Your CuraLink platform is now live! 🎉**
