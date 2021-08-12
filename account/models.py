from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """
     Model for user account
    """

    class Meta:
        db_table = 'account'
        abstract = False

    provider = models.CharField(max_length=50, default='email')

    def __str__(self) -> str:
        return f'pk: {self.pk}, username: {self.username}, email: {self.email} provider: {self.provider}'
