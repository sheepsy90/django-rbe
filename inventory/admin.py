from django.contrib import admin

# Register your models here.
from inventory.models import Object, Event

admin.site.register(Object)
admin.site.register(Event)
