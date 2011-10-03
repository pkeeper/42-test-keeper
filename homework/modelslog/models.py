from django.db import models
from django.db.utils import DatabaseError
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class SignalLog(models.Model):
    """
        Model for log entries for signal processor
    """
    MODEL_ACTIONS = (('Create', 'Create'),
                     ('Change', 'Change'),
                     ('Delete', 'Delete'),)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    action = models.CharField(max_length=10, choices=MODEL_ACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.action + ': ' + self.content_type.app_label + '.' + \
            self.content_type.model


def process_signal(sender, **kwargs):
    """
        Signal processor that logs Create, Change and Delete events
        for site-registered models
    """
    obj = kwargs['instance']
    obj_content = ContentType.objects.get_for_model(obj)
    # Do not log unnecessary things)
    if obj_content.model_class() is SignalLog:
        return
    if obj_content.app_label in ('admin', 'sessions'):
        return

    if kwargs['signal'] == signals.post_save:
        if 'created' in kwargs:
            if kwargs['created']:
                s = SignalLog(action='Create', content_object=obj)
            else:
                s = SignalLog(action='Change', content_object=obj)
    if kwargs['signal'] == signals.post_delete:
        s = SignalLog(action='Delete', content_object=obj)
    try:
        s.save()
    except DatabaseError:
        print "Signal for " + obj_content.app_label + "." + obj_content.model
        print "Can't save log. DatabaseError\n"
    return


# Listen signals
signals.post_save.connect(process_signal)
signals.post_delete.connect(process_signal)
