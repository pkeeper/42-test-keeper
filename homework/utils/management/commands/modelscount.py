from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db.utils import ConnectionDoesNotExist
from django.db import DEFAULT_DB_ALIAS

from optparse import make_option


class Command(BaseCommand):
    help = 'Count objects of each registered model'
    args = '[appname appname ...]'
    option_list = BaseCommand.option_list + (
            make_option('--database', action='store', dest='database',
                        default=DEFAULT_DB_ALIAS,
                        help='Nominates a specific database to dump fixtures'
                        ' from. Defaults to the "default" database.'),)

    def handle(self, *app_labels, **options):
        db = options.get('database', DEFAULT_DB_ALIAS)
        if not app_labels:
            # If no apps provided - use all
            try:
                ctypes = ContentType.objects.using(db).all()
                # This is to force LazzyQuery try to get objects
                for t in ctypes:
                    pass
            except ConnectionDoesNotExist, e:
                raise CommandError("%s. Wrong database alias?" % e)
        else:
            from django.db import models
            try:
                [models.get_app(app_label) for app_label in app_labels]
            except (ImproperlyConfigured, ImportError), e:
                raise CommandError("%s. Are you sure your INSTALLED_APPS"
                                   " setting is correct?" % e)
            ctypes = []
            for app in app_labels:
                try:
                    for ctype in ContentType.objects.using(db)\
                                  .filter(app_label=app):
                        ctypes.append(ctype)
                except ConnectionDoesNotExist, e:
                    raise CommandError("%s. Wrong database alias?" % e)
                except ObjectDoesNotExist, e:
                    raise CommandError("%s. There is no ContentType record for"
                                       " this app" % e)
        output = ''
        err_output = ''
        for ctype in ctypes:
            model_class = ctype.model_class()
            try:
                description = '''Application : %s
                Model : %s
                Objects count: %s\n''' % (ctype.app_label, ctype.model,
                                          model_class.objects.count())
            except:
                description = '''You seem to have legacy ContentType record for
                            deleted model '%s' of application : '%s'\n''' % (
                                                ctype.model, ctype.app_label)
            output += description
            err_output += 'Error: ' + description
        self.stdout.write(output)
        self.stderr.write(err_output)
