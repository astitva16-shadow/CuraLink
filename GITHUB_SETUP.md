# GitHub Repository Setup Guide

## 📦 Pushing CuraLink to GitHub

Your repository: https://github.com/astitva16-shadow/CuraLink.git

---

## 🚀 Initial Setup (First Time)

### 1. Initialize Git (if not already done)
```bash
cd d:\Astitva\CuraLink
git init
```

### 2. Add Remote Repository
```bash
git remote add origin https://github.com/astitva16-shadow/CuraLink.git
```

### 3. Configure Git (if not already done)
```bash
git config user.name "Astitva"
git config user.email "your-email@example.com"
```

### 4. Add All Files
```bash
git add .
```

### 5. Create Initial Commit
```bash
git commit -m "Initial commit: CuraLink healthcare platform with PWA support"
```

### 6. Push to GitHub
```bash
# For first push
git branch -M main
git push -u origin main
```

---

## 🔄 Regular Updates

### After making changes:

```bash
# Check what's changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Your descriptive message here"

# Push to GitHub
git push
```

---

## 📝 Commit Message Examples

Good commit messages:
```bash
git commit -m "Add PWA support with service worker and manifest"
git commit -m "Implement GPS-based hospital finder with 100km radius"
git commit -m "Import 50+ real Indian hospitals from government data"
git commit -m "Add dark mode toggle and animations across all pages"
git commit -m "Fix: Resolve service worker caching issue"
git commit -m "Update: Improve hospital search performance"
```

---

## 🌿 Branch Management

### Create Feature Branch
```bash
git checkout -b feature/new-feature-name
# Work on your feature
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature-name
```

### Switch Back to Main
```bash
git checkout main
```

### Merge Feature Branch
```bash
git checkout main
git merge feature/new-feature-name
git push
```

---

## 📋 What's Already Set Up

### ✅ Files Ready for GitHub:
- `.gitignore` - Excludes unnecessary files
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- All source code
- PWA assets (manifest, service worker, icons)
- Database migrations
- Static files
- Documentation files

### ❌ Files Excluded (via .gitignore):
- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `db.sqlite3` - Local database
- `*.pyc` - Compiled Python files
- `.env` - Environment variables
- `media/` - Uploaded files
- IDE settings (`.vscode/`, `.idea/`)

---

## 🔐 Environment Variables

### For Production (GitHub Secrets or .env):

Create a `.env` file (not committed to Git):
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### GitHub Secrets (for CI/CD):
1. Go to repository Settings
2. Secrets and variables → Actions
3. Add secrets:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `ALLOWED_HOSTS`

---

## 📦 Release Workflow

### Create a Release:

1. **Tag your version**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **On GitHub:**
   - Go to Releases
   - Click "Create a new release"
   - Choose your tag
   - Write release notes
   - Publish release

---

## 🤝 Collaboration Workflow

### If Working with Team:

1. **Clone repository**
   ```bash
   git clone https://github.com/astitva16-shadow/CuraLink.git
   ```

2. **Create branch for your work**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes and commit**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

4. **Push and create Pull Request**
   ```bash
   git push -u origin feature/your-feature
   ```
   Then create PR on GitHub

5. **Review and merge**
   - Team reviews PR
   - Merge to main branch

---

## 🔧 Useful Git Commands

### Check Status
```bash
git status
```

### View Commit History
```bash
git log --oneline --graph --all
```

### Undo Last Commit (keep changes)
```bash
git reset --soft HEAD~1
```

### Discard Local Changes
```bash
git checkout -- filename
```

### Pull Latest Changes
```bash
git pull origin main
```

### View Differences
```bash
git diff
```

### List Branches
```bash
git branch -a
```

### Delete Branch
```bash
git branch -d feature/branch-name
```

---

## 📊 GitHub Actions (CI/CD)

### Create `.github/workflows/django.yml`:

```yaml
name: Django CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run migrations
      run: |
        python manage.py migrate
    
    - name: Run tests
      run: |
        python manage.py test
```

---

## 🎯 Repository Structure on GitHub

```
CuraLink/
├── .github/
│   └── workflows/
│       └── django.yml
├── accounts/
├── appointments/
├── hospitals/
├── symptoms/
├── api/
├── templates/
├── static/
│   ├── icons/
│   ├── manifest.json
│   └── service-worker.js
├── data/
├── curalink/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── LICENSE
└── Documentation files
```

---

## 📝 Adding a License

### MIT License (Recommended):

Create `LICENSE` file:
```
MIT License

Copyright (c) 2025 Astitva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🌟 Making Your Repo Stand Out

### Add to README:
- Badges (build status, coverage, etc.)
- Screenshots
- Demo link
- Video walkthrough

### Add Files:
- `CONTRIBUTING.md` - Contribution guidelines
- `CODE_OF_CONDUCT.md` - Community guidelines
- `CHANGELOG.md` - Version history
- `SECURITY.md` - Security policy

### GitHub Settings:
- Add topics/tags (django, pwa, healthcare, etc.)
- Add description
- Add website link
- Enable Issues for bug tracking
- Enable Discussions for community

---

## 🐛 Troubleshooting

### Large Files Error
```bash
# Remove large file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/large/file" \
  --prune-empty --tag-name-filter cat -- --all
```

### Merge Conflicts
```bash
# See conflicts
git status

# Edit conflicted files
# Then:
git add .
git commit -m "Resolve merge conflicts"
```

### Reset to Remote
```bash
git fetch origin
git reset --hard origin/main
```

---

## ✅ Pre-Push Checklist

Before pushing to GitHub:
- [ ] All tests pass
- [ ] No sensitive data in code
- [ ] .gitignore is correct
- [ ] README is updated
- [ ] Requirements.txt is current
- [ ] Commit messages are clear
- [ ] Code is documented
- [ ] No debug code left

---

## 🚀 Quick Push Commands

```bash
# Quick update workflow
cd d:\Astitva\CuraLink
git add .
git commit -m "Update: Your message here"
git push

# First time setup
git init
git remote add origin https://github.com/astitva16-shadow/CuraLink.git
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## 📱 GitHub Mobile App

- Install GitHub app on your phone
- View commits, issues, PRs on the go
- Merge pull requests
- Review code

---

## 🎓 Learning Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Your repository is ready for GitHub! 🎉**

Run the quick push commands above to upload CuraLink to your repository.
