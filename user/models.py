from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    role=models.CharField(default="member",blank=True,null=True)
    email_token=models.UUIDField(default=uuid.uuid4,blank=True,null=True)