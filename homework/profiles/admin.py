from profiles.models import Profile, ContactField
from django.contrib import admin


class ContactFieldInline(admin.StackedInline):
    model = ContactField
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    inlines = [ContactFieldInline]

admin.site.register(Profile,ProfileAdmin)