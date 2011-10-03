# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RequestEntry'
        db.create_table('requests_requestentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('params', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('headers', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('requests', ['RequestEntry'])


    def backwards(self, orm):
        
        # Deleting model 'RequestEntry'
        db.delete_table('requests_requestentry')


    models = {
        'requests.requestentry': {
            'Meta': {'object_name': 'RequestEntry'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'headers': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'params': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['requests']
