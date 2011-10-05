from django.contrib import admin
from models import RequestEntry


class RequestLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(RequestEntry, RequestLogAdmin)
