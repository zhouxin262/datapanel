# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'GroupTime', fields ['dateline', 'datetype']
        db.create_unique('datapanel_grouptime', ['dateline', 'datetype'])


    def backwards(self, orm):
        # Removing unique constraint on 'GroupTime', fields ['dateline', 'datetype']
        db.delete_unique('datapanel_grouptime', ['dateline', 'datetype'])


    models = {
        'datapanel.grouptime': {
            'Meta': {'unique_together': "(('datetype', 'dateline'),)", 'object_name': 'GroupTime'},
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['datapanel']