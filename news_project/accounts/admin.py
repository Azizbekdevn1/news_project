from django.contrib import admin
from .models import Profile

#1 -way register this admin
#admin.site.register(Profile)
#2-way register this admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['photo', 'birthdate', 'user']

admin.site.register(Profile,ProfileAdmin)