from django.db import models
from django.db.models import signals


class SignalLog(models.Model):
    MODEL_ACTIONS = (('Create', 'Create'),
                     ('Change', 'Change'),
                     ('Delete', 'Delete'),)
    model_app = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    model_id = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=MODEL_ACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)


def process_signal(sender, **kwargs):
    obj = kwargs['instance']

    # Do not log unnecessary things)
    if obj.__class__ is SignalLog:
        return
    if obj._meta.app_label == 'admin':
        return

    if kwargs['signal'] == signals.post_save:
        if 'created' in kwargs:
            if kwargs['created']:
                s = SignalLog(action='Create', model_app=obj._meta.app_label,
                          model=obj.__class__.__name__, model_id=obj.id)
                s.save()
                return
        s = SignalLog(action='Change', model_app=obj._meta.app_label,
                  model=obj.__class__.__name__, model_id=obj.id)
        s.save()
        return
    if kwargs['signal'] == signals.post_delete:
        s = SignalLog(action='Delete', model_app=obj._meta.app_label,
                  model=obj.__class__.__name__, model_id=obj.id)
        s.save()


# Listen signals
signals.post_save.connect(process_signal)
signals.post_delete.connect(process_signal)
