# Google OAuth Setup Guide for CuraLink

This guide explains how to set up Google OAuth authentication for CuraLink.

## 🔑 Step 1: Create Google OAuth Credentials

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 2. Create a New Project (or select existing)
- Click on project dropdown at the top
- Click "New Project"
- Name: `CuraLink` (or your preferred name)
- Click "Create"

### 3. Enable Google+ API
- Go to "APIs & Services" → "Library"
- Search for "Google+ API"
- Click on it and click "Enable"

### 4. Create OAuth Consent Screen
- Go to "APIs & Services" → "OAuth consent screen"
- Choose "External" user type
- Click "Create"
- Fill in the required fields:
  - **App name**: CuraLink
  - **User support email**: Your email
  - **Developer contact email**: Your email
- Click "Save and Continue"
- Skip scopes (click "Save and Continue")
- Skip test users (click "Save and Continue")
- Click "Back to Dashboard"

### 5. Create OAuth 2.0 Credentials
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth client ID"
- Choose "Web application"
- Configure:
  - **Name**: CuraLink Web Client
  - **Authorized JavaScript origins**:
    - For local development: `http://localhost:8000`
    - For production: `https://your-domain.onrender.com`
  - **Authorized redirect URIs**:
    - For local development: `http://localhost:8000/accounts/google/login/callback/`
    - For production: `https://your-domain.onrender.com/accounts/google/login/callback/`
- Click "Create"

### 6. Save Your Credentials
You'll get:
- **Client ID**: Something like `123456789-abcdefg.apps.googleusercontent.com`
- **Client Secret**: Something like `GOCSPX-abc123def456`

**Keep these secure!** You'll need them for configuration.

---

## 🔧 Step 2: Configure CuraLink

### For Local Development

1. **Create `.env` file** in project root:
```bash
# .env
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

2. **Update settings.py** to read from .env:
```python
from decouple import config

# In SOCIALACCOUNT_PROVIDERS
'APP': {
    'client_id': config('GOOGLE_CLIENT_ID', default=''),
    'secret': config('GOOGLE_CLIENT_SECRET', default=''),
    'key': ''
}
```

3. **Install django-allauth**:
```bash
pip install django-allauth
```

4. **Run migrations**:
```bash
python manage.py migrate
```

5. **Create superuser** (if not already):
```bash
python manage.py createsuperuser
```

### For Production (Render)

Add these environment variables in Render dashboard:

```bash
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
```

**Important**: Make sure to add your production domain to Google Console's Authorized redirect URIs:
```
https://your-app.onrender.com/accounts/google/login/callback/
```

---

## 🚀 Step 3: Configure Django Admin

### 1. Run the server:
```bash
python manage.py runserver
```

### 2. Login to Django Admin:
Visit: http://localhost:8000/admin/

### 3. Add Social Application:
- Go to "Sites" → Click on "example.com"
- Change domain to: `localhost:8000` (for development)
- Change display name to: `CuraLink Local`
- Save

- Go to "Social Applications" → Click "Add Social Application"
- Fill in:
  - **Provider**: Google
  - **Name**: Google OAuth
  - **Client id**: Paste your Google Client ID
  - **Secret key**: Paste your Google Client Secret
  - **Sites**: Select "localhost:8000" (or your site) and move to "Chosen sites"
- Click "Save"

---

## 🎯 Step 4: Test Google Login

### 1. Logout from Django admin
Visit: http://localhost:8000/

### 2. Click "Login"
You should see the "Sign in with Google" button

### 3. Click "Sign in with Google"
- You'll be redirected to Google login
- Choose your Google account
- Grant permissions
- You'll be redirected back to CuraLink

### 4. Check your account:
- You should be automatically logged in
- A new user account is created with your Google email

---

## 🔒 Security Best Practices

### 1. Never Commit Credentials
Make sure `.env` is in `.gitignore`:
```
# .gitignore
.env
*.pyc
__pycache__/
db.sqlite3
```

### 2. Use Different Credentials for Production
- Create separate OAuth credentials for production
- Never use development credentials in production

### 3. Restrict Authorized Domains
In Google Console, only authorize your actual domains:
- Development: `localhost:8000`
- Production: `your-app.onrender.com`

---

## 🐛 Troubleshooting

### Error: "Redirect URI mismatch"
**Solution**: Make sure the redirect URI in Google Console exactly matches:
```
http://localhost:8000/accounts/google/login/callback/
```
Note: Must end with `/`

### Error: "Social account not found"
**Solution**: 
1. Go to Django admin
2. Check "Social Applications" is configured
3. Make sure site is added to "Chosen sites"

### Error: "Client ID not found"
**Solution**:
1. Verify environment variables are set correctly
2. Restart Django server after adding environment variables

### Google Login Button Not Showing
**Solution**:
1. Check django-allauth is installed: `pip list | grep allauth`
2. Verify migrations ran: `python manage.py migrate`
3. Clear browser cache

---

## 📱 How Google Login Works

1. **User clicks "Sign in with Google"**
2. **Redirected to Google** for authentication
3. **User grants permissions** to CuraLink
4. **Google redirects back** with authorization code
5. **Django exchanges code** for user info
6. **User account created/updated** automatically
7. **User logged in** to CuraLink

---

## 🎨 Customizing Social Login

### Custom Callback (Optional)

Create `accounts/views.py` to customize behavior:

```python
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from accounts.models import Patient

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    """Auto-create Patient profile for Google login users"""
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        if not hasattr(user, 'patient_profile'):
            Patient.objects.create(user=user)
```

---

## ✅ Configuration Checklist

- [ ] Google Cloud project created
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created
- [ ] Client ID and Secret saved securely
- [ ] Authorized redirect URIs added
- [ ] django-allauth installed
- [ ] Migrations run
- [ ] Social Application added in Django admin
- [ ] Site configured correctly
- [ ] Tested Google login flow
- [ ] Environment variables set for production

---

## 🌐 Production Deployment Checklist

### Render Environment Variables
```bash
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
```

### Google Console Settings
- Add production domain to authorized origins:
  ```
  https://your-app.onrender.com
  ```
- Add production callback URL:
  ```
  https://your-app.onrender.com/accounts/google/login/callback/
  ```

### Django Admin (Production)
1. Login to: `https://your-app.onrender.com/admin/`
2. Update Site: Change from "example.com" to "your-app.onrender.com"
3. Add Social Application with production credentials

---

**🎉 Google OAuth is now configured! Users can sign in with their Google accounts.**
