from django.contrib import admin

# Register your models here.
from inventory.models import Object, ObjectLogEntry


admin.site.register(Object)
admin.site.register(ObjectLogEntry)
