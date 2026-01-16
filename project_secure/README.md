# Communication_LTD - Secure Version

✅ Secure implementation with protections against SQL injection and XSS attacks.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py migrate

# Run server
python manage.py runserver

# Access: http://127.0.0.1:8000/
```

## Security Features

### SQL Injection Protection
- **Django ORM**: Parameterized queries automatically
- **Example**: `User.objects.get(username=username)` instead of raw SQL

### XSS Protection
- **HTML Escaping**: All user input escaped before storage
- **Example**: `escape(client_name)` converts `<script>` to `&lt;script&gt;`

### Password Security
- **Hashing**: HMAC + SHA256 + random salt per user
- **Policy**: Min 10 chars, uppercase, lowercase, digit, special character
- **History**: Cannot reuse last 3 passwords
- **Locking**: Account locks after 3 failed login attempts
- **Dictionary**: Blocks common passwords from `common_passwords.txt`

### Password Reset
- **SHA-1 verification codes**: Sent via email (file-based for development)
- **Codes saved to**: `sent_emails/` folder

## Test Security

### SQL Injection (Blocked)
1. Login with username: `admin' OR '1'='1`
2. Result: "User not found" ✓ (treated as literal text)

### XSS (Blocked)
1. Add client with name: `<script>alert('XSS')</script>`
2. Result: Displays as text, no JavaScript execution ✓

## Project Structure

```
project_secure/
├── Communication_LTD/
│   ├── models.py          # Database: User, Client, PasswordHistory, ResetCode
│   ├── views.py           # SECURE: Django ORM + escape()
│   ├── utils.py           # Password validation, HMAC hashing
│   ├── templates/         # HTML files
│   └── static/            # CSS
├── config/settings.py     # Django configuration
├── passwordConfig.json    # Password policy rules
└── common_passwords.txt   # Blocked passwords list
```

## Key Security Code

### Login (Safe from SQLi)
```python
user = User.objects.get(username=username)  # Django ORM
```

### Dashboard (Safe from XSS)
```python
from django.utils.html import escape
client_name = escape(request.POST.get("client_name"))
Client.objects.create(name=client_name, ...)
```

## Password Configuration

Edit `passwordConfig.json`:
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
