from django.contrib import admin

from organizations.models import OrganizationTag, Organization, OrganizationUser, OrganizationCheck, \
    OrganizationDescription

class OrganizationAdmin(admin.ModelAdmin):
    model = OrganizationTag
    filter_horizontal = ('tags',)

admin.site.register(OrganizationTag)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser)
admin.site.register(OrganizationCheck)
admin.site.register(OrganizationDescription)
