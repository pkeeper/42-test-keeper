# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SignalLog'
        db.create_table('modelslog_signallog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_app', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('obj_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('modelslog', ['SignalLog'])


    def backwards(self, orm):
        
        # Deleting model 'SignalLog'
        db.delete_table('modelslog_signallog')


    models = {
        'modelslog.signallog': {
            'Meta': {'object_name': 'SignalLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'model_app': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'obj_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['modelslog']
