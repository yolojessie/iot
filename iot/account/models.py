from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fullName = models.CharField(max_length=128)
    address = models.CharField(max_length=128, blank=True, null=True)
    webPushP256dh = models.TextField(blank=True, null=True)                         # webpush key p256dh
    webPushAuth = models.TextField(blank=True, null=True)                           # webpush key auth
    webPushEndpoint = models.TextField(blank=True, null=True)                       # webpush endpoint
    keyword = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.fullName + ' (' + self.username + ')'