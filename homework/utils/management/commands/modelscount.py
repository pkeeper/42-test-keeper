from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Count objects of each registered model'

    def handle(self, *args, **options):
        for ctype in ContentType.objects.all():
            self.stdout.write('Application : %s\n' % ctype.app_label)
            self.stdout.write('Model : %s\n' % ctype.model)
            self.stdout.write('Objects : %s\n\n' %
                              ctype.model_class().objects.count())
