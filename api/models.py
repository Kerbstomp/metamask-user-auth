from django.db import models

from .utils import get_new_nonce


class User(models.Model):
    username = models.TextField(null=False, blank=True)
    public_address = models.TextField(null=False, unique=True, blank=False)
    nonce = models.BigIntegerField(null=False, default=get_new_nonce)
    created_datetime = models.DateTimeField(auto_now_add=True)
    