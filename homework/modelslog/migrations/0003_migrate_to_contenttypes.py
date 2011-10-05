# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        # Migrate model data
        for log_entry in orm.SignalLog.objects.all():
            if log_entry.model_app is None:
                continue
            log_entry.content_type = orm['contenttypes.ContentType'].objects.get(
                                                    app_label=log_entry.model_app,
                                                    model=log_entry.model)
            log_entry.object_id = log_entry.obj_id
            log_entry.save()

    def backwards(self, orm):
        # Migrate model data
        for log_entry in orm.SignalLog.objects.all():
            if log_entry.content_type is None:
                continue
            log_entry.model_app = log_entry.content_type.app_label
            log_entry.model = log_entry.content_type.model
            log_entry.obj_id = log_entry.object_id
            log_entry.save()

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'modelslog.signallog': {
            'Meta': {'object_name': 'SignalLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'model_app': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['modelslog']
