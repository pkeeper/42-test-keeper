from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


def print_apps():
    """
        Returns output for 'modelscount' django-admin command
        it's easier to test this way
    """
    out = ''
    err_out = ''
    for ctype in ContentType.objects.all():
        description = '''Application : %s
        Model : %s
        Objects count: %s\n''' % (ctype.app_label, ctype.model,
                                  ctype.model_class().objects.count())
        out += description
        err_out += 'error: ' + description
    return out, err_out


class Command(BaseCommand):
    help = 'Count objects of each registered model'

    def handle(self, *args, **options):
            out, err_out = print_apps()
            self.stdout.write(out)
            self.stderr.write(err_out)
