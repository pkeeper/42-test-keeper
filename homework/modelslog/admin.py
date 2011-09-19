from django.contrib import admin
from models import SignalLog


class SignalLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(SignalLog, SignalLogAdmin)
