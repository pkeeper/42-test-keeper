from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType


class SignalLog(models.Model):
    """
    Model for log entries for signal processor
    """
    MODEL_ACTIONS = (('Create', 'Create'),
                     ('Change', 'Change'),
                     ('Delete', 'Delete'),)
    model_app = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    obj_id = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=MODEL_ACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.action + ': ' + self.model_app + '.' + self.model


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
                s = SignalLog(action='Create', model_app=obj_content.app_label,
                          model=obj_content.model, obj_id=obj.id)
                s.save()
                return
        s = SignalLog(action='Change', model_app=obj_content.app_label,
                          model=obj_content.model, obj_id=obj.id)
        s.save()
        return
    if kwargs['signal'] == signals.post_delete:
        s = SignalLog(action='Delete', model_app=obj_content.app_label,
                          model=obj_content.model, obj_id=obj.id)
        s.save()


# Listen signals
signals.post_save.connect(process_signal)
signals.post_delete.connect(process_signal)
