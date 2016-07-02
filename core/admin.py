from django.contrib import admin

# Register your models here.
from core.models import PasswordResetKey
from core.models import Profile
from core.models import RegistrationKey

admin.site.register(PasswordResetKey)
admin.site.register(Profile)
admin.site.register(RegistrationKey)
