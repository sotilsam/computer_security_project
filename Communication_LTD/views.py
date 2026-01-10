from django.utils.html import escape
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape
from .models import User, Client, ResetCode
from .utils import check_password_rules, hash_password, hash_code
import os
import random
from django.core.mail import send_mail
from django.conf import settings
import secrets
import hashlib


import secrets
import hashlib

def generate_sha1_code():
    #Create random bytes, then derive a SHA-1 based code
    seed = secrets.token_bytes(32)
    code = hashlib.sha1(seed).hexdigest()[:8].upper()
    return code

def sha1_hex(text: str) -> str:
    # Hash user input with SHA-1 for storage/compare
    return hashlib.sha1(text.encode("utf-8")).hexdigest()



# LOGIN

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("login") 

        hashed, _ = hash_password(password, user.salt)

        if hashed != user.password_hash:
            messages.error(request, "Incorrect password")
            return redirect("login") 

        request.session["username"] = username
        return redirect("dashboard")

    return render(request, "login.html") 


# REGISTER

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

        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, "Username or email already used")
            return redirect("register")

        hashed, salt = hash_password(password)

        User.objects.create(
            username=username,
            email=email,
            password_hash=hashed,
            salt=salt
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")



# DASHBOARD

def dashboard_view(request):
    if "username" not in request.session:
        return redirect("login")

    username = request.session["username"]
    user = User.objects.get(username=username)

    if request.method == "POST":
        client_name = request.POST.get("client_name", "").strip()
        client_email = request.POST.get("client_email", "").strip()
        client_phone = request.POST.get("client_phone", "").strip()

        if not client_name:
            messages.error(request, "Client name is required")
            return redirect("dashboard")

        Client.objects.create(
            name=client_name,
            email=client_email,
            phone=client_phone,

        )

        messages.success(request, "Client added successfully")
        return redirect("dashboard")

    clients = Client.objects.all() 

    return render(request, "dashboard.html", {
        "username": user.username,
        "clients": clients,
    })

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
            username=username,
            defaults={"code_hash": code_hash}
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

        valid, msg = check_password_rules(password)
        if not valid:
            messages.error(request, msg)
            return redirect("reset_password")

        user = User.objects.get(username=username)
        hashed, salt = hash_password(password)

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

                # DEBUG 1
        print("DEBUG USER:", username, "id:", user.id)
        print("DEBUG BEFORE:", user.password_hash[:12], "salt:", str(user.salt)[:12])


        hashed_old, _ = hash_password(old, user.salt)
        if hashed_old != user.password_hash:
            messages.error(request, "Incorrect, old password")
            return redirect("change_password")

        valid, msg = check_password_rules(new)
        if not valid:
            messages.error(request, msg)
            return redirect("change_password")

        if new != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("change_password")

        hashed, salt = hash_password(new)
        user.password_hash = hashed
        user.salt = salt
        user.save()

                # DEBUG 2
        user.refresh_from_db()
        print("DEBUG AFTER:", user.password_hash[:12], "salt:", str(user.salt)[:12])

        messages.success(request, "Password changed successfully")
        return redirect("dashboard")

    return render(request, "change_password.html")
