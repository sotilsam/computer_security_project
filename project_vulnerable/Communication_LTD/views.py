"""
VULNERABLE VERSION 
This version contains intentional security vulnerabilities:
1. SQL Injection in login, register, and dashboard
2. Stored XSS in dashboard (client name display)
3. No input sanitization
"""

import hashlib
import os
import random
import secrets

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Client, PasswordHistory, ResetCode, User
from .utils import check_password_rules, hash_code, hash_password, load_password_rules


def generate_sha1_code():
    # Create random bytes, then derive a SHA-1 based code
    seed = secrets.token_bytes(32)
    code = hashlib.sha1(seed).hexdigest()[:8].upper()
    return code


def sha1_hex(text: str) -> str:
    # Hash user input with SHA-1 for storage/compare
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# LOGIN - VULNERABLE TO SQL INJECTION


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # STEP 1: Get salt for the user (first query)
        # VULNERABLE: SQL Injection - using raw SQL without parameterization
        with connection.cursor() as cursor:
            query = (
                f"SELECT salt FROM Communication_LTD_user WHERE username = '{username}'"
            )
            cursor.execute(query)
            salt_row = cursor.fetchone()

        if not salt_row:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        salt = salt_row[0]

        # STEP 2: Hash the password with the retrieved salt
        hashed, _ = hash_password(password, salt)

        # STEP 3: Query for user with this username AND password hash (VULNERABLE!)
        # VULNERABLE: SQL Injection - checking both username and password in one query
        # This allows bypass with: admin' --
        with connection.cursor() as cursor:
            query = f"SELECT id, username, email, failed_login_attempts, is_locked FROM Communication_LTD_user WHERE username = '{username}' AND password_hash = '{hashed}'"
            cursor.execute(query)
            row = cursor.fetchone()

        # Check if login failed (wrong password)
        rules = load_password_rules()
        max_attempts = rules.get("max_failed_logins", 3)

        if not row:
            # Wrong password - increment failed attempts for this user
            with connection.cursor() as cursor:
                # Get current failed attempts
                query = f"SELECT id, failed_login_attempts, is_locked FROM Communication_LTD_user WHERE username = '{username}'"
                cursor.execute(query)
                user_data = cursor.fetchone()

            if user_data:
                user_id, failed_attempts, is_locked = user_data
                failed_attempts += 1
                new_is_locked = 1 if failed_attempts >= max_attempts else 0

                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE Communication_LTD_user SET failed_login_attempts = {failed_attempts}, is_locked = {new_is_locked} WHERE id = {user_id}")

                if new_is_locked:
                    messages.error(request, f"Account locked due to {max_attempts} failed login attempts. Contact administrator.")
                else:
                    remaining = max_attempts - failed_attempts
                    messages.error(request, f"Invalid username or password. {remaining} attempts remaining.")
            else:
                messages.error(request, "Invalid username or password")

            return redirect("login")

        user_id, db_username, _email, failed_attempts, is_locked = row

        # Check if user is locked
        if is_locked:
            messages.error(
                request,
                f"Account locked due to {max_attempts} failed login attempts. Contact administrator.",
            )
            return redirect("login")

        # Successful login - reset failed attempts
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE Communication_LTD_user SET failed_login_attempts = 0 WHERE id = {user_id}"
            )

        request.session["username"] = db_username
        return redirect("dashboard")

    return render(request, "login.html")


# REGISTER - VULNERABLE TO SQL INJECTION


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        valid, msg = check_password_rules(password)
        if not valid:
            messages.error(request, msg)
            return redirect("register")

        # VULNERABLE: SQL Injection - checking if user exists
        # NO ESCAPING - allows SQL injection!
        with connection.cursor() as cursor:
            query = f"SELECT COUNT(*) FROM Communication_LTD_user WHERE username = '{username}' OR email = '{email}'"
            cursor.execute(query)
            count = cursor.fetchone()[0]

        if count > 0:
            messages.error(request, "Username or email already used")
            return redirect("register")

        hashed, salt = hash_password(password)

        # VULNERABLE: SQL Injection - inserting user
        # NO ESCAPING - allows SQL injection!
        with connection.cursor() as cursor:
            query = f"INSERT INTO Communication_LTD_user (username, email, password_hash, salt, failed_login_attempts, is_locked) VALUES ('{username}', '{email}', '{hashed}', '{salt}', 0, 0)"
            cursor.execute(query)

        # Get the user we just created for password history
        user = User.objects.get(username=username)

        # Save password to history
        PasswordHistory.objects.create(user=user, password_hash=hashed, salt=salt)

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")


# DASHBOARD - VULNERABLE TO STORED XSS AND SQL INJECTION


def dashboard_view(request):
    if "username" not in request.session:
        return redirect("login")

    username = request.session["username"]
    user = User.objects.get(username=username)

    if request.method == "POST":
        client_name = request.POST.get("client_name", "").strip()
        # VULNERABLE: No XSS sanitization - user can inject HTML/JavaScript
        # Example: <script>alert('XSS')</script>

        client_email = request.POST.get("client_email", "").strip()
        client_phone = request.POST.get("client_phone", "").strip()

        if not client_name:
            messages.error(request, "Client name is required")
            return redirect("dashboard")

        # VULNERABLE: SQL Injection - using raw SQL
        # NO ESCAPING - allows SQL injection!
        with connection.cursor() as cursor:
            query = f"INSERT INTO Communication_LTD_client (name, email, phone) VALUES ('{client_name}', '{client_email}', '{client_phone}')"
            cursor.execute(query)

        messages.success(request, "Client added successfully")
        return redirect("dashboard")

    clients = Client.objects.all()

    return render(
        request,
        "dashboard.html",
        {
            "username": user.username,
            "clients": clients,
        },
    )


# LOGOUT


def logout_view(request):
    request.session.flush()
    return redirect("login")


# FORGOT PASSWORD — SEND CODE


def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()

        user = User.objects.filter(username=username).first()
        if not user:
            messages.error(request, "User not found")
            return redirect("forgot_password")

        code = generate_sha1_code()
        code_hash = sha1_hex(code)

        ResetCode.objects.update_or_create(
            username=username, defaults={"code_hash": code_hash}
        )

        # English comment: Send the plain code, store only the hash
        send_mail(
            subject="Password reset code",
            message=f"Your verification code is: {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        request.session["reset_username"] = username
        messages.success(request, "Code generated")
        return redirect("verify")

    return render(request, "forgot_password.html")


# VERIFY CODE


def verify_code_view(request):
    if request.method == "POST":
        code_input = request.POST.get("code", "").strip().upper()

        username = request.session.get("reset_username")
        if not username:
            messages.error(request, "Please request a new code")
            return redirect("forgot_password")

        reset_obj = ResetCode.objects.filter(username=username).first()
        if not reset_obj:
            messages.error(request, "Invalid request")
            return redirect("forgot_password")

        if sha1_hex(code_input) != reset_obj.code_hash:
            messages.error(request, "Incorrect code")
            return redirect("verify")

        request.session["reset_verified"] = True
        return redirect("reset_password")

    return render(request, "verify.html")


# RESET PASSWORD (AFTER FORGOT)


def reset_password_view(request):
    if "reset_username" not in request.session:
        if not request.session.get("reset_verified"):
            messages.error(request, "Please verify the code first")
            return redirect("verify")

        if "reset_username" not in request.session:
            return redirect("forgot_password")

    username = request.session["reset_username"]

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        user = User.objects.get(username=username)

        # Check password rules including history
        valid, msg = check_password_rules(password, user=user)
        if not valid:
            messages.error(request, msg)
            return redirect("reset_password")

        hashed, salt = hash_password(password)

        # Save old password to history before updating
        PasswordHistory.objects.create(
            user=user, password_hash=user.password_hash, salt=user.salt
        )

        user.password_hash = hashed
        user.salt = salt
        user.save()

        request.session.pop("reset_username", None)
        request.session.pop("reset_verified", None)
        messages.success(request, "Password reset successfully")
        return redirect("login")

    return render(request, "reset_password.html")


# CHANGE PASSWORD (LOGGED IN)


def change_password_view(request):
    if "username" not in request.session:
        return redirect("login")

    username = request.session["username"]
    user = User.objects.get(username=username)

    if request.method == "POST":
        old = request.POST.get("old_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm")

        hashed_old, _ = hash_password(old, user.salt)
        if hashed_old != user.password_hash:
            messages.error(request, "Incorrect, old password")
            return redirect("change_password")

        # Check password rules including history
        valid, msg = check_password_rules(new, user=user)
        if not valid:
            messages.error(request, msg)
            return redirect("change_password")

        if new != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("change_password")

        hashed, salt = hash_password(new)

        # Save old password to history before updating
        PasswordHistory.objects.create(
            user=user, password_hash=user.password_hash, salt=user.salt
        )

        user.password_hash = hashed
        user.salt = salt
        user.save()

        messages.success(request, "Password changed successfully")
        return redirect("dashboard")

    return render(request, "change_password.html")
