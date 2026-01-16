# Communication_LTD - Vulnerable Version

⚠️ **WARNING**: Intentional security vulnerabilities for educational demonstration. DO NOT USE IN PRODUCTION!

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

## Vulnerabilities Included

### 1. SQL Injection
- **Login**: Raw SQL with 2-query authentication (get salt → check credentials)
- **Register**: Raw SQL for duplicate checking and user insertion
- **Dashboard**: Raw SQL for client insertion

### 2. Stored XSS
- **Dashboard**: No input sanitization + `| safe` filter in template
- **Impact**: JavaScript executes for all users viewing the client list

## SQL Injection Demo

### Attack: Authentication Bypass

**Current Implementation:**
1. Query 1: Get salt for username
2. Hash password with retrieved salt
3. Query 2: Check username AND password_hash

**Payload:**
- **Username**: `admin' --`
- **Password**: (anything)

**How it works:**
```sql
-- Query 1
SELECT salt FROM ... WHERE username = 'admin' --'
-- Comment removes trailing quote, gets admin's salt ✓

-- Query 2
SELECT ... WHERE username = 'admin' --' AND password_hash = 'hash'
-- Comment removes password check entirely!
-- Becomes: SELECT ... WHERE username = 'admin'
-- Logs in without valid password! ✓
```

**Result**: Successfully logged in as admin without knowing the password!

**Try in secure version**: Same input → "Invalid username or password" (treated as literal text)

## XSS Demo

### Attack: Stored XSS

**Payload (avoid quotes to prevent SQL crash):**
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<b style=color:red>HACKED</b>
```

**Steps:**
1. Login to dashboard
2. Add client with malicious name
3. Submit form
4. JavaScript executes immediately and on every page load

**Why it works:**
```python
# views.py - No sanitization
client_name = request.POST.get("client_name")
```

```html
<!-- dashboard.html - Renders HTML -->
<li>{{ c.name | safe }}</li>
```

**Try in secure version**: Same input → Displayed as text (escaped to `&lt;script&gt;`)

## Vulnerable Code Locations

### SQL Injection Points

**Login** ([views.py:46](Communication_LTD/views.py#L46)):
```python
query = f"SELECT salt FROM Communication_LTD_user WHERE username = '{username}'"
```

**Login** ([views.py:63](Communication_LTD/views.py#L63)):
```python
query = f"SELECT ... WHERE username = '{username}' AND password_hash = '{hashed}'"
```

**Register** ([views.py:112](Communication_LTD/views.py#L112)):
```python
query = f"SELECT COUNT(*) FROM ... WHERE username = '{username}' OR email = '{email}'"
```

**Dashboard** ([views.py:168](Communication_LTD/views.py#L168)):
```python
query = f"INSERT INTO ... VALUES ('{client_name}', '{client_email}', '{client_phone}')"
```

### XSS Points

**Dashboard Input** ([views.py:163](Communication_LTD/views.py#L163)):
```python
client_name = request.POST.get("client_name", "").strip()  # No escaping
```

**Dashboard Output** ([templates/dashboard.html:54](Communication_LTD/templates/dashboard.html#L54)):
```html
<li>{{ c.name | safe }} — {{ c.email }} — {{ c.phone }}</li>
```

## Demonstration Checklist

### SQL Injection
- [ ] Login with `admin' --` → Successfully logged in ✓
- [ ] Compare with secure version → Login fails ✓
- [ ] Screenshot both results

### Stored XSS
- [ ] Add client: `<script>alert(1)</script>` → Alert popup ✓
- [ ] Refresh page → Alert persists (stored in DB) ✓
- [ ] Compare with secure version → Displayed as text ✓
- [ ] Screenshot both results

## Failed Login Tracking

Note: SQL injection bypass still tracks failed attempts for normal wrong passwords:
- Wrong password → Increments counter, shows "X attempts remaining"
- 3 failed attempts → Account locked
- SQLi with `admin' --` → Bypasses entirely, no tracking

## Project Structure

```
project_vulnerable/
├── Communication_LTD/
│   ├── models.py          # Same as secure version
│   ├── views.py           # VULNERABLE: Raw SQL, no escaping
│   ├── utils.py           # Same password validation (Part A features)
│   ├── templates/
│   │   └── dashboard.html # Uses | safe filter
│   └── static/
├── config/settings.py
├── passwordConfig.json
└── common_passwords.txt
```

## Comparison with Secure Version

| Aspect | Vulnerable | Secure |
|--------|-----------|--------|
| Login | 2 raw SQL queries with f-strings | Django ORM |
| Register | Raw SQL with f-strings | Django ORM |
| Dashboard | Raw SQL with f-strings | Django ORM |
| Input | No sanitization | `escape()` function |
| Template | `\| safe` on raw data | `\| safe` on escaped data |

## ⚠️ DISCLAIMER

**FOR EDUCATIONAL USE ONLY**

This code demonstrates common web security vulnerabilities. Never deploy vulnerable code to production environments. Use only for learning, testing, and security presentations.
