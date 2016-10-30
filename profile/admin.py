from django.contrib import admin

from profile.models import UserProfile, LanguageSpoken

admin.site.register(UserProfile)
admin.site.register(LanguageSpoken)
