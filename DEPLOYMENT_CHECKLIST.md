# 🚀 CuraLink Deployment Quick Reference

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Generate secure SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up DATABASE_URL (PostgreSQL)
- [ ] Configure superuser credentials (optional)

### 2. Dependencies
- [ ] Install all requirements: `pip install -r requirements.txt`
- [ ] Verify Python version: 3.10+

### 3. Database
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Import hospital data: `python manage.py import_hospitals`

### 4. Static Files
- [ ] Collect static files: `python manage.py collectstatic --no-input`
- [ ] Verify Whitenoise middleware in settings.py

### 5. Security
- [ ] SECRET_KEY changed from default
- [ ] DEBUG=False in production
- [ ] HTTPS/SSL enabled
- [ ] Security headers configured

---

## Quick Commands

### Local Testing
```bash
# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Import hospital data
python manage.py import_hospitals

# Create superuser
python manage.py createsuperuser

# Run with Gunicorn (test production server)
gunicorn curalink.wsgi:application
```

### Generate SECRET_KEY
```python
import secrets
print(secrets.token_urlsafe(50))
```

---

## Platform-Specific Quick Start

### Render
1. Create PostgreSQL database
2. Create Web Service from GitHub repo
3. Build command: `chmod +x build.sh && ./build.sh`
4. Start command: `gunicorn curalink.wsgi:application`
5. Set environment variables (see below)

### Railway
1. Deploy from GitHub repo
2. Add PostgreSQL database
3. Railway auto-configures DATABASE_URL
4. Set other environment variables

### Heroku
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY=xxx DEBUG=False
git push heroku main
```

### PythonAnywhere
1. Clone repo in bash console
2. Create virtualenv: `mkvirtualenv curalink --python=python3.10`
3. Install requirements: `pip install -r requirements.txt`
4. Configure Web app manually
5. Set up static files mapping

---

## Essential Environment Variables

```bash
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=secure-password
DJANGO_SUPERUSER_EMAIL=admin@curalink.com
```

---

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --no-input
# Check STATIC_ROOT and STATICFILES_STORAGE in settings.py
```

### Database connection error
- Verify DATABASE_URL is correct
- Check PostgreSQL service is running
- Run migrations: `python manage.py migrate`

### 500 Error
- Check application logs
- Verify all environment variables are set
- Ensure ALLOWED_HOSTS includes your domain

### Import hospital data failed
```bash
# Re-run import command
python manage.py import_hospitals

# Check if CSV file exists
ls data/india_hospitals.csv
```

---

## Post-Deployment Verification

- [ ] Homepage loads (https://your-domain.com/)
- [ ] Admin panel accessible (/admin/)
- [ ] Hospital finder shows data
- [ ] Map displays with markers
- [ ] Dark mode toggle works
- [ ] PWA installable on mobile
- [ ] Appointments can be created
- [ ] GPS location access works

---

## Useful URLs

- **GitHub Repo**: https://github.com/astitva16-shadow/CuraLink
- **Full Guide**: See DEPLOYMENT_GUIDE.md
- **PWA Setup**: See PWA_SETUP_GUIDE.md
- **Features**: See FEATURES_LIST.md

---

**Need detailed instructions? Check DEPLOYMENT_GUIDE.md**
