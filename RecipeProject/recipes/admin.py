from django.contrib import admin

from .models import Recipe, Cuisine, Message
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Cuisine)
admin.site.register(Message)
