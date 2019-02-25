from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserType(models.Model):
    user_type=models.CharField(max_length=100,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
