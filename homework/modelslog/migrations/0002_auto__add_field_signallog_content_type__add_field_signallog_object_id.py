# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SignalLog.content_type'
        db.add_column('modelslog_signallog', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True), keep_default=False)

        # Adding field 'SignalLog.object_id'
        db.add_column('modelslog_signallog', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SignalLog.content_type'
        db.delete_column('modelslog_signallog', 'content_type_id')

        # Deleting field 'SignalLog.object_id'
        db.delete_column('modelslog_signallog', 'object_id')


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
