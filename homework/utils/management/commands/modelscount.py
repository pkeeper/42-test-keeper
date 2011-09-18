from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Count objects of each registered model'

    def handle(self, *args, **options):
        for ctype in ContentType.objects.all():
            description = '''Application : %s
            Model : %s 
            Objects count: %s\n''' % (ctype.app_label, ctype.model, ctype.model_class().objects.count())

            self.stdout.write(description)
            self.stderr.write('error: ' + description)
