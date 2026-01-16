import hashlib
import hmac
import os
import json
from django.conf import settings

#פונקציה להמרת קובץ גסון
def load_password_rules():
    config_path = settings.BASE_DIR / "passwordConfig.json"
    with open(config_path, "r") as f:
        return json.load(f)


def load_common_passwords():
    """Load common passwords dictionary from file"""
    dict_path = settings.BASE_DIR / "common_passwords.txt"
    try:
        with open(dict_path, "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def check_password_rules(password, user=None):
    """
    Validate password against rules in passwordConfig.json
    Also checks password history and common passwords dictionary
    """
    rules = load_password_rules()
#  ככה רולס נראה עכשיו וככה אפשר להשתמש בנתונים שלו בפונקציה - dict
# rules = {
#     "min_length": 10,
#     "complexity": {
#         "uppercase": True,
#         "lowercase": True,
#         "digits": True,
#         "special": True
#     },
#     "history_count": 3,
#     "max_failed_logins": 3,
#     "prevent_reuse": True
# }

    # Check length
    if len(password) < rules["min_length"]:
        return False, f"Password must be at least {rules['min_length']} characters"

    # Check complexity
    if rules["complexity"]["uppercase"] and not any(c.isupper() for c in password):
        return False, "Password must include uppercase letter"

    if rules["complexity"]["lowercase"] and not any(c.islower() for c in password):
        return False, "Password must include lowercase letter"

    if rules["complexity"]["digits"] and not any(c.isdigit() for c in password):
        return False, "Password must include a digit"

    special_chars = "!@#$%^&*()-_=+{}[]"
    if rules["complexity"]["special"] and not any(c in special_chars for c in password):
        return False, "Password must include special character"

    # Check against common passwords dictionary
    common_passwords = load_common_passwords()
    if password.lower() in common_passwords:
        return False, "Password is too common. Please choose a stronger password"

    # Check password history (prevent reuse of last N passwords)
    if user and rules.get("prevent_reuse", False):
        from .models import PasswordHistory
        history_count = rules.get("history_count", 3)

        # Get last N password hashes
        previous_passwords = PasswordHistory.objects.filter(
            user=user
        ).order_by('-created_at')[:history_count]

        # Check if new password matches any previous passwords
        for prev in previous_passwords:
            prev_hash, _ = hash_password(password, prev.salt)
            if prev_hash == prev.password_hash:
                return False, f"Password was used recently. Cannot reuse last {history_count} passwords"

    return True, "OK"


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()

    hashed = hmac.new(
        salt.encode(),
        password.encode(),
        hashlib.sha256
    ).hexdigest()

    return hashed, salt


def hash_code(code):
    return hashlib.sha1(code.encode()).hexdigest()
