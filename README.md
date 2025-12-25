# Communication LTD

A Django-based secure portal for user authentication, password reset via verification codes, and a simple client management dashboard.

## Features
- Register and login users
- Change password while logged in
- Forgot password flow with a verification code (code stored as a SHA-1 hash)
- Dashboard to add clients and view a shared client list

## Tech Stack
- Python
- Django
- SQLite (default)

## Getting Started

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows (PowerShell)
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4) Start the server
```bash
python manage.py runserver
```

Then open: `http://127.0.0.1:8000/`

## Email Configuration (Password Reset)
If your reset flow sends emails, configure Django email settings in `settings.py`, for example:
- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS` or `EMAIL_USE_SSL`

## Notes on Hashing
This project uses SHA-1 for verification code hashing to match course requirements. In real production systems, prefer stronger approaches like HMAC or SHA-256, and store only hashed codes with short expirations.

## Project Structure (high level)
- `Communication_LTD/`: app (views, models, templates, static)
- `config/`: Django project settings and URLs
- `db.sqlite3`: local development database (auto-created)

## Screenshots
Add screenshots here:
- `screenshots/dashboard.png`
- `screenshots/change_password.png`

## License
For academic and learning use.
