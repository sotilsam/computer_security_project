# Communication_LTD - SECURE VERSION

## ✅ This is the SECURE version with protections against:
- SQL Injection (using Django ORM)
- Cross-Site Scripting / XSS (using escape() function)
- Weak passwords (complex password requirements)
- Password reuse (password history tracking)
- Brute force login (account locking after 3 attempts)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database
python manage.py makemigrations
python manage.py migrate

# 3. Run server
python manage.py runserver

# 4. Open browser
http://127.0.0.1:8000/
```

## Features

### Part A - Secure Development
1. ✅ **User Registration** - with HMAC + Salt encryption
2. ✅ **Complex Password** - from passwordConfig.json
3. ✅ **Change Password** - validates old password
4. ✅ **Login System** - with account locking
5. ✅ **Dashboard** - add/view clients (XSS protected)
6. ✅ **Forgot Password** - SHA-1 verification codes via email

### Security Features
- **Password Encryption**: HMAC + SHA-256 + random salt
- **Password History**: Prevents reusing last 3 passwords
- **Failed Login Limit**: Locks account after 3 wrong passwords
- **Dictionary Check**: Blocks common passwords from list
- **SQL Injection Protection**: Django ORM (parameterized queries)
- **XSS Protection**: HTML escaping on all user inputs

## Security Implementation

### Protection Against SQL Injection

**Secure code example:**
```python
# Uses Django ORM - automatically parameterized
user = User.objects.get(username=username)

# Behind the scenes:
# SQL: SELECT * FROM users WHERE username = ?
# Parameters: [username]
```

### Protection Against XSS

**Secure code example:**
```python
from django.utils.html import escape

client_name = escape(request.POST.get("client_name"))
# <script> becomes &lt;script&gt; (displayed as text)
```

## Password Configuration

Edit `passwordConfig.json` to change password requirements:

```json
{
    "min_length": 10,
    "complexity": {
        "uppercase": true,
        "lowercase": true,
        "digits": true,
        "special": true
    },
    "history_count": 3,
    "max_failed_logins": 3,
    "prevent_reuse": true
}
```

## Project Structure

```
project_secure/
├── Communication_LTD/      # Main application
│   ├── models.py           # Database structure
│   ├── views.py            # Business logic (SECURE)
│   ├── utils.py            # Password validation & encryption
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML files
│   └── static/             # CSS, images
├── config/                 # Project settings
├── manage.py               # Django CLI tool
├── passwordConfig.json     # Password policy
├── common_passwords.txt    # Blocked passwords
└── requirements.txt        # Python dependencies
```

## Testing

### Test Password Validation

Try registering with weak passwords:

1. `abc` → "Password must be at least 10 characters"
2. `abcdefghij` → "Password must include uppercase letter"
3. `Abcdefghij` → "Password must include a digit"
4. `Abcdefghi1` → "Password must include special character"
5. `password` → "Password is too common"
6. `Test123!@#` → ✅ Success!

### Test Password History

1. Register with password: `FirstPass1!`
2. Login and change to: `SecondPass2@`
3. Change again to: `ThirdPass3#`
4. Change again to: `FourthPass4$`
5. Try to change back to: `SecondPass2@`
6. Result: "Cannot reuse last 3 passwords"

### Test Account Locking

1. Register a user
2. Logout
3. Try to login with wrong password 3 times
4. Result: "Account locked due to 3 failed login attempts"
5. Even correct password won't work now

### Test SQL Injection Protection

1. On login page, try username: `admin' OR '1'='1`
2. Result: "User not found" (attack blocked!)
3. The quote is treated as part of the username string

### Test XSS Protection

1. Login
2. Add client with name: `<script>alert('XSS')</script>`
3. Result: Displays as text, script doesn't execute
4. You'll see: `&lt;script&gt;alert('XSS')&lt;/script&gt;`

## Email Configuration

Currently using file-based email backend (for development):
- Emails saved to: `sent_emails/` folder
- Each email is a `.txt` file

To use real SMTP (production), edit `config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Database

Using SQLite (file-based database):
- File: `db.sqlite3`
- To reset database: Delete file and run migrations again

```bash
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

## For Submission

This is the **SECURE version** for Part B of the assignment.

**Demonstrates:**
- ✅ Protection against SQL Injection (Section 4 of Part B)
- ✅ Protection against XSS (Section 3 of Part B)
- ✅ All Part A requirements implemented

**Compare with:**
- `../project_vulnerable/` - Shows vulnerabilities
- See `../COMPLETE_GUIDE_ENGLISH.md` for detailed explanations

## License

For academic use only.
