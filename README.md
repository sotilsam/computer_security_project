# Communication_LTD - Cyber Security Project

Web application security demonstration for a telecommunications company, showing both vulnerable and secure implementations.

## Project Structure

```
computer_security_project/
├── project_secure/         # Secure implementation (Django ORM, input sanitization)
└── project_vulnerable/     # Vulnerable implementation (raw SQL, no sanitization)
```

## Features

- User registration with password policy enforcement
- Login with account locking (3 failed attempts)
- Password change with history tracking (prevents reuse of last 3 passwords)
- Password reset via email verification code (SHA-1)
- Client management dashboard
- Password hashing: HMAC + SHA256 + Salt

## Security Demonstrations

### Vulnerable Version
- **SQL Injection**: Raw SQL queries allow authentication bypass
- **Stored XSS**: Unsanitized input stored and displayed with `| safe` filter

### Secure Version
- **SQL Injection Protection**: Django ORM with parameterized queries
- **XSS Protection**: HTML escaping with `escape()` before storage

## Quick Start

### 1. Setup (Both Versions)

```bash
# Navigate to either project folder
cd project_secure/  # or project_vulnerable/

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py makemigrations

python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### 2. Access Application

- **Main app**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

## SQL Injection Demo (Vulnerable Version)

### Attack: Authentication Bypass

**Username:** `admin' --`
**Password:** (anything)

**How it works:**
1. Query 1: `SELECT salt FROM ... WHERE username = 'admin' --'`
   - Gets admin's salt (comment `--` removes trailing quote)
2. Query 2: `SELECT ... WHERE username = 'admin' --' AND password_hash = '...'`
   - Comment `--` removes password check
   - Logs in without valid password!

**Try in secure version:** Same input is treated as literal username → Login fails ✓

## XSS Demo (Vulnerable Version)

### Attack: Stored XSS

1. Login to dashboard
2. Add client with name: `<script>alert('XSS')</script>`
3. Submit form
4. JavaScript executes for all users viewing the list

**Avoid quotes in payload** to prevent SQL crashes:
- `<script>alert(1)</script>` ✓
- `<img src=x onerror=alert(1)>` ✓
- `<b style=color:red>HACKED</b>` ✓

**Try in secure version:** Input is escaped to `&lt;script&gt;...` → Displayed as text ✓

## Password Policy

Configured in `passwordConfig.json`:
- Minimum 10 characters
- Must include: uppercase, lowercase, digit, special character
- Cannot reuse last 3 passwords
- Account locks after 3 failed login attempts
- Dictionary check against `common_passwords.txt`

## Email Configuration

Uses file-based email backend (development):
- Emails saved to `sent_emails/` folder
- No external service required
- Check files to see verification codes

## Key Code Differences

### Login (SQL Injection)

**Vulnerable:**
```python
query = f"SELECT salt FROM ... WHERE username = '{username}'"
cursor.execute(query)
```

**Secure:**
```python
user = User.objects.get(username=username)  # Django ORM
```

### Dashboard (XSS)

**Vulnerable:**
```python
client_name = request.POST.get("client_name")  # No sanitization
# Template: {{ c.name | safe }}  # Renders HTML
```

**Secure:**
```python
from django.utils.html import escape
client_name = escape(request.POST.get("client_name"))  # Sanitized
# Template: {{ c.name | safe }}  # Safe because input is escaped
```

## Assignment Requirements

✅ **Part A**: Password policy, HMAC+Salt, password history, account locking
✅ **Part B**: Separate vulnerable/secure versions demonstrating SQLi and XSS

## Notes

- Clients are global (not per-user) - acceptable per assignment requirements
- SHA-1 used only for temporary verification codes (assignment requirement)
- HMAC+SHA256 used for password hashing (secure)
- Database resets on migration changes

