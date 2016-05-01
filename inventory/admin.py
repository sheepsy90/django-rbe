from django.contrib import admin

# Register your models here.
from inventory.models import Object, Event, Tag

admin.site.register(Object)
admin.site.register(Tag)
admin.site.register(Event)
