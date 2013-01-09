# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'GroupTime', fields ['datetype', 'dateline']
        db.delete_unique('datapanel_grouptime', ['datetype', 'dateline'])

        # Deleting model 'GroupTime'
        db.delete_table('datapanel_grouptime')

        # Adding model 'Timeline'
        db.create_table('datapanel_timeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('datapanel', ['Timeline'])

        # Adding unique constraint on 'Timeline', fields ['datetype', 'dateline']
        db.create_unique('datapanel_timeline', ['datetype', 'dateline'])


    def backwards(self, orm):
        # Removing unique constraint on 'Timeline', fields ['datetype', 'dateline']
        db.delete_unique('datapanel_timeline', ['datetype', 'dateline'])

        # Adding model 'GroupTime'
        db.create_table('datapanel_grouptime', (
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('datapanel', ['GroupTime'])

        # Adding unique constraint on 'GroupTime', fields ['datetype', 'dateline']
        db.create_unique('datapanel_grouptime', ['datetype', 'dateline'])

        # Deleting model 'Timeline'
        db.delete_table('datapanel_timeline')


    models = {
        'datapanel.timeline': {
            'Meta': {'unique_together': "(('datetype', 'dateline'),)", 'object_name': 'Timeline'},
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['datapanel']