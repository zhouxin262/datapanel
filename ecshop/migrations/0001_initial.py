# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrderInfo'
        db.create_table('ecshop_orderinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esc_orderinfo', to=orm['project.Project'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esc_orderinfo', to=orm['session.Session'])),
            ('order_sn', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('order_amount', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=11, decimal_places=3)),
        ))
        db.send_create_signal('ecshop', ['OrderInfo'])

        # Adding model 'OrderGoods'
        db.create_table('ecshop_ordergoods', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esc_ordergoods', to=orm['project.Project'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esc_ordergoods', to=orm['session.Session'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esc_ordergoods', to=orm['ecshop.OrderInfo'])),
            ('goods_id', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('goods_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('ecshop', ['OrderGoods'])


    def backwards(self, orm):
        # Deleting model 'OrderInfo'
        db.delete_table('ecshop_orderinfo')

        # Deleting model 'OrderGoods'
        db.delete_table('ecshop_ordergoods')


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
        'ecshop.ordergoods': {
            'Meta': {'object_name': 'OrderGoods'},
            'goods_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'goods_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esc_ordergoods'", 'to': "orm['ecshop.OrderInfo']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esc_ordergoods'", 'to': "orm['project.Project']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esc_ordergoods'", 'to': "orm['session.Session']"})
        },
        'ecshop.orderinfo': {
            'Meta': {'object_name': 'OrderInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '11', 'decimal_places': '3'}),
            'order_sn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esc_orderinfo'", 'to': "orm['project.Project']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esc_orderinfo'", 'to': "orm['session.Session']"})
        },
        'project.project': {
            'Meta': {'ordering': "['-lastview']", 'unique_together': "(('name', 'creator'),)", 'object_name': 'Project'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'create_project'", 'to': "orm['auth.User']"}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'lastview': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participate_projects'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'referrer.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'referrer.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'session.session': {
            'Meta': {'object_name': 'Session'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['session.UserAgent']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['session.UserDevice']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['session.UserOS']"}),
            'permanent_session_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'session'", 'null': 'True', 'blank': 'True', 'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['referrer.Keyword']"}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['referrer.Site']"}),
            'session_key': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'user_timezone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'session.useragent': {
            'Meta': {'unique_together': "(('family', 'major', 'minor', 'patch'),)", 'object_name': 'UserAgent'},
            'family': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'minor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'patch': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        },
        'session.userdevice': {
            'Meta': {'unique_together': "(('family', 'is_mobile', 'is_spider'),)", 'object_name': 'UserDevice'},
            'family': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_spider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'session.useros': {
            'Meta': {'unique_together': "(('family', 'major', 'minor', 'patch', 'patch_minor'),)", 'object_name': 'UserOS'},
            'family': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'minor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'patch': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'patch_minor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        }
    }

    complete_apps = ['ecshop']