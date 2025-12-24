from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    def __str__(self):
        return self.username




class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name



class ResetCode(models.Model):
    username = models.CharField(max_length=100, unique=True)
    code_hash = models.CharField(max_length=40) # SHA-1 hex is 40 chars
    created_at = models.DateTimeField(auto_now_add=True)