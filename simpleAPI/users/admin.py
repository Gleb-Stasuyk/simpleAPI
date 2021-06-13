from django.contrib import admin

from .models import Profile
from django.contrib.auth import get_user_model

class ProfileAdmin(admin.ModelAdmin):
    #search_fields = ('user',)
    empty_value_display = '-пусто-'

admin.site.register(Profile, ProfileAdmin)