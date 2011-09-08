from django.contrib import admin
from profiles.models import Profile, ContactField


class ContactFieldInline(admin.StackedInline):
    model = ContactField
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    inlines = [ContactFieldInline]

admin.site.register(Profile,ProfileAdmin)