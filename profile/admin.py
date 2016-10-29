from django.contrib import admin

from profile.models import InvitationKey, UserProfile, LanguageSpoken

admin.site.register(InvitationKey)
admin.site.register(UserProfile)
admin.site.register(LanguageSpoken)
