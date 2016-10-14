from django.contrib import admin

# Register your models here.
from oidc_provider.models import UserConsent
from core.models import PasswordResetKey

admin.site.register(PasswordResetKey)
admin.site.register(UserConsent)
