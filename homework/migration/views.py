from django.http import HttpResponse
from django.core.management import call_command

from south.migration import Migrations
from south.hacks import hacks
from StringIO import StringIO

def clear_cache():
    hacks.clear_app_cache()
    hacks.repopulate_app_cache()
    # And also clear our cached Migration classes
    Migrations._clear_cache()

def migrate(request,id):
    if id == '1':
        call_command("migrate", "profiles", delete_ghosts=True)
        call_command("convert_to_south", "profiles")
    elif id == '2':
        call_command("syncdb", noinput=True)
    elif id == '3':
        call_command("schemamigration", "profiles", auto=True)
        clear_cache()
        call_command("migrate", "profiles", no_initial_data=True)
    return HttpResponse("OK")