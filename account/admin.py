from django.contrib import admin

from account.models import Account


@admin.register(Account)
class AccountModelAdmin(admin.ModelAdmin):
    """
    Display table account on admin panel
    """

    pass
