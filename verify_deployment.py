"""
CuraLink Deployment Verification Script

This script verifies that all deployment configurations are correct
and that the application is ready for production deployment.
"""

import os
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")

def check_file(filename, description):
    """Check if a file exists"""
    if Path(filename).exists():
        print(f"{GREEN}✓{RESET} {description}: {filename}")
        return True
    else:
        print(f"{RED}✗{RESET} {description}: {filename} - NOT FOUND")
        return False

def check_content(filename, search_text, description):
    """Check if a file contains specific text"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_text in content:
                print(f"{GREEN}✓{RESET} {description}")
                return True
            else:
                print(f"{RED}✗{RESET} {description} - NOT FOUND")
                return False
    except FileNotFoundError:
        print(f"{RED}✗{RESET} {description} - FILE NOT FOUND: {filename}")
        return False

def main():
    print_header("CuraLink Deployment Verification")
    
    all_checks = []
    
    # Check deployment files
    print(f"\n{YELLOW}Checking Deployment Files:{RESET}")
    all_checks.append(check_file('Procfile', 'Procfile'))
    all_checks.append(check_file('runtime.txt', 'Python runtime specification'))
    all_checks.append(check_file('build.sh', 'Build script'))
    all_checks.append(check_file('requirements.txt', 'Requirements file'))
    all_checks.append(check_file('.env.example', 'Environment variables template'))
    
    # Check documentation files
    print(f"\n{YELLOW}Checking Documentation:{RESET}")
    all_checks.append(check_file('DEPLOYMENT_GUIDE.md', 'Deployment guide'))
    all_checks.append(check_file('DEPLOYMENT_CHECKLIST.md', 'Deployment checklist'))
    all_checks.append(check_file('DEPLOYMENT_SUMMARY.md', 'Deployment summary'))
    
    # Check settings.py configuration
    print(f"\n{YELLOW}Checking Django Settings Configuration:{RESET}")
    all_checks.append(check_content(
        'curalink/settings.py',
        'import dj_database_url',
        'Database URL parsing import'
    ))
    all_checks.append(check_content(
        'curalink/settings.py',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'Whitenoise middleware'
    ))
    all_checks.append(check_content(
        'curalink/settings.py',
        "os.environ.get('SECRET_KEY'",
        'Environment-based SECRET_KEY'
    ))
    all_checks.append(check_content(
        'curalink/settings.py',
        "os.environ.get('DEBUG'",
        'Environment-based DEBUG'
    ))
    all_checks.append(check_content(
        'curalink/settings.py',
        "os.environ.get('ALLOWED_HOSTS'",
        'Environment-based ALLOWED_HOSTS'
    ))
    all_checks.append(check_content(
        'curalink/settings.py',
        "if 'DATABASE_URL' in os.environ:",
        'PostgreSQL DATABASE_URL support'
    ))
    all_checks.append(check_content(
        'curalink/settings.py',
        'SECURE_SSL_REDIRECT',
        'Production security settings'
    ))
    
    # Check requirements.txt packages
    print(f"\n{YELLOW}Checking Deployment Packages:{RESET}")
    all_checks.append(check_content(
        'requirements.txt',
        'gunicorn',
        'Gunicorn web server'
    ))
    all_checks.append(check_content(
        'requirements.txt',
        'whitenoise',
        'Whitenoise static files'
    ))
    all_checks.append(check_content(
        'requirements.txt',
        'dj-database-url',
        'Database URL parser'
    ))
    all_checks.append(check_content(
        'requirements.txt',
        'psycopg2-binary',
        'PostgreSQL adapter'
    ))
    
    # Check Procfile configuration
    print(f"\n{YELLOW}Checking Procfile Configuration:{RESET}")
    all_checks.append(check_content(
        'Procfile',
        'gunicorn curalink.wsgi',
        'Gunicorn command in Procfile'
    ))
    
    # Check runtime.txt
    print(f"\n{YELLOW}Checking Python Runtime:{RESET}")
    all_checks.append(check_content(
        'runtime.txt',
        'python-3.10',
        'Python 3.10 specification'
    ))
    
    # Check build.sh
    print(f"\n{YELLOW}Checking Build Script:{RESET}")
    all_checks.append(check_content(
        'build.sh',
        'collectstatic',
        'Static files collection'
    ))
    all_checks.append(check_content(
        'build.sh',
        'migrate',
        'Database migrations'
    ))
    all_checks.append(check_content(
        'build.sh',
        'import_hospitals',
        'Hospital data import'
    ))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100
    
    print(f"Tests Passed: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print(f"\n{GREEN}✓ All deployment checks passed!{RESET}")
        print(f"{GREEN}✓ CuraLink is ready for production deployment!{RESET}")
        print(f"\nNext steps:")
        print(f"1. Review DEPLOYMENT_GUIDE.md for platform-specific instructions")
        print(f"2. Generate a secure SECRET_KEY")
        print(f"3. Choose your deployment platform (Render/Railway/Heroku/PythonAnywhere)")
        print(f"4. Set environment variables")
        print(f"5. Deploy!")
        return 0
    else:
        print(f"\n{RED}✗ Some deployment checks failed!{RESET}")
        print(f"{YELLOW}Please review the errors above and fix them before deploying.{RESET}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
