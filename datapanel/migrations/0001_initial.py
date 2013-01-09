# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupTime'
        db.create_table('datapanel_grouptime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('datapanel', ['GroupTime'])


    def backwards(self, orm):
        # Deleting model 'GroupTime'
        db.delete_table('datapanel_grouptime')


    models = {
        'datapanel.grouptime': {
            'Meta': {'object_name': 'GroupTime'},
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['datapanel']