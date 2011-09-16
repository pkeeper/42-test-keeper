from django.conf import settings


def add_settings(request):
    return {'SETTINGS': settings}
