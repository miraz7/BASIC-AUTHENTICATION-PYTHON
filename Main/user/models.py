from django.db import models
from django.contrib.auth.models import User
import uuid

class user(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    firstname=models.CharField(max_length=255, blank=True)
    lastname=models.CharField(max_length=255, blank= True)
    address=models.CharField(max_length=255, blank= True)
    validation_code=models.CharField(max_length=255)
    verified=models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True, auto_now_add=False)


class login_sessions(models.Model):
    email=models.EmailField()
    access_token=models.CharField(max_length=255)
    refresh_token=models.CharField(max_length=255)
    is_invalidated=models.BooleanField()
    logged_in_at=models.DateTimeField(auto_now=False, auto_now_add=False )
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True, auto_now_add=False)