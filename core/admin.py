from django.contrib import admin

# Register your models here.
from oidc_provider.models import UserConsent
from core.models import PasswordResetKey, Toggles, EmailVerification

admin.site.register(PasswordResetKey)
admin.site.register(UserConsent)
admin.site.register(EmailVerification)


class ClassAdmin(admin.ModelAdmin):
    filter_horizontal = ('activated_for',)

    def save_model(self, request, obj, form, change):
        # First we save the object and after that we invalidate the cache
        obj.save()

        # Invalidate the cache after that
        Toggles.invalidate_cache(obj.toggle_name)

    def delete_model(self, request, obj):
        # First we save the object and after that we invalidate the cache
        toggle_name = obj.toggle_name
        obj.delete()

        # Invalidate the cache after that
        Toggles.invalidate_cache(toggle_name)

admin.site.register(Toggles, ClassAdmin)

