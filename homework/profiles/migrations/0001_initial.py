# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('bio', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('profiles', ['Profile'])

        # Adding model 'ContactField'
        db.create_table('profiles_contactfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['profiles.Profile'])),
            ('contact_type', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='type')),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('profiles', ['ContactField'])


    def backwards(self, orm):
        
        # Deleting model 'Profile'
        db.delete_table('profiles_profile')

        # Deleting model 'ContactField'
        db.delete_table('profiles_contactfield')


    models = {
        'profiles.contactfield': {
            'Meta': {'object_name': 'ContactField'},
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['profiles.Profile']"}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['profiles']
