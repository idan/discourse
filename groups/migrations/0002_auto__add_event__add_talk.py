# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('groups_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['groups.InterestGroup'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('registration', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('groups', ['Event'])

        # Adding model 'Talk'
        db.create_table('groups_talk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='talks', to=orm['groups.Event'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('groups', ['Talk'])


    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('groups_event')

        # Deleting model 'Talk'
        db.delete_table('groups_talk')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'groups.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['groups.InterestGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'groups.interestgroup': {
            'Meta': {'object_name': 'InterestGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'interest_groups'", 'symmetrical': 'False', 'through': "orm['groups.Membership']", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '70', 'blank': 'True'})
        },
        'groups.membership': {
            'Meta': {'object_name': 'Membership'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.InterestGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'groups.talk': {
            'Meta': {'object_name': 'Talk'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['groups.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['groups']
