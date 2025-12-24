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


def check_password_rules(password):
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

    if len(password) < rules["min_length"]:
        return False, "Password too short"
    
    if rules["complexity"]["uppercase"] and not any(c.isupper() for c in password):
        return False, "Password must include uppercase letter"

    if rules["complexity"]["lowercase"] and not any(c.islower() for c in password):
        return False, "Password must include lowercase letter"

    if rules["complexity"]["digits"] and not any(c.isdigit() for c in password):
        return False, "Password must include a digit"
    
    special_chars = "!@#$%^&*()-_=+{}[]"
    if rules["complexity"]["special"] and not any(c in special_chars for c in password):
        return False, "Password must include special character"

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
