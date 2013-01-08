# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserAgent'
        db.create_table('session_useragent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('major', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('minor', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('patch', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
        ))
        db.send_create_signal('session', ['UserAgent'])

        # Adding unique constraint on 'UserAgent', fields ['family', 'major', 'minor', 'patch']
        db.create_unique('session_useragent', ['family', 'major', 'minor', 'patch'])

        # Adding model 'UserOS'
        db.create_table('session_useros', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('major', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('minor', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('patch', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('patch_minor', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
        ))
        db.send_create_signal('session', ['UserOS'])

        # Adding unique constraint on 'UserOS', fields ['family', 'major', 'minor', 'patch', 'patch_minor']
        db.create_unique('session_useros', ['family', 'major', 'minor', 'patch', 'patch_minor'])

        # Adding model 'UserDevice'
        db.create_table('session_userdevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('is_mobile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_spider', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('session', ['UserDevice'])

        # Adding unique constraint on 'UserDevice', fields ['family', 'is_mobile', 'is_spider']
        db.create_unique('session_userdevice', ['family', 'is_mobile', 'is_spider'])

        # Adding model 'Session'
        db.create_table('session_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='session', null=True, blank=True, to=orm['project.Project'])),
            ('session_key', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=40)),
            ('permanent_session_key', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user_language', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('user_timezone', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session', null=True, to=orm['session.UserAgent'])),
            ('os', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session', null=True, to=orm['session.UserOS'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session', null=True, to=orm['session.UserDevice'])),
            ('referrer_site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session', null=True, to=orm['referrer.Site'])),
            ('referrer_keyword', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session', null=True, to=orm['referrer.Keyword'])),
            ('track_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ipaddress', self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15)),
        ))
        db.send_create_signal('session', ['Session'])

        # Adding model 'SessionValue'
        db.create_table('session_sessionvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='value', to=orm['session.Session'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('session', ['SessionValue'])

        # Adding model 'GTime'
        db.create_table('session_gtime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessiongroupbytime', to=orm['project.Project'])),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('track_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('session', ['GTime'])

        # Adding unique constraint on 'GTime', fields ['datetype', 'dateline']
        db.create_unique('session_gtime', ['datetype', 'dateline'])

        # Adding model 'GReferrerSite'
        db.create_table('session_greferrersite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessiongroupbyReferrerSite', to=orm['project.Project'])),
            ('referrer_site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='GReferrerSite', null=True, to=orm['referrer.Site'])),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('track_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('session', ['GReferrerSite'])

        # Adding model 'GReferrerKeyword'
        db.create_table('session_greferrerkeyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessiongroupbyReferrerkeyword', to=orm['project.Project'])),
            ('referrer_keyword', self.gf('django.db.models.fields.related.ForeignKey')(related_name='GReferrerKeyword', null=True, to=orm['referrer.Keyword'])),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('track_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('session', ['GReferrerKeyword'])


    def backwards(self, orm):
        # Removing unique constraint on 'GTime', fields ['datetype', 'dateline']
        db.delete_unique('session_gtime', ['datetype', 'dateline'])

        # Removing unique constraint on 'UserDevice', fields ['family', 'is_mobile', 'is_spider']
        db.delete_unique('session_userdevice', ['family', 'is_mobile', 'is_spider'])

        # Removing unique constraint on 'UserOS', fields ['family', 'major', 'minor', 'patch', 'patch_minor']
        db.delete_unique('session_useros', ['family', 'major', 'minor', 'patch', 'patch_minor'])

        # Removing unique constraint on 'UserAgent', fields ['family', 'major', 'minor', 'patch']
        db.delete_unique('session_useragent', ['family', 'major', 'minor', 'patch'])

        # Deleting model 'UserAgent'
        db.delete_table('session_useragent')

        # Deleting model 'UserOS'
        db.delete_table('session_useros')

        # Deleting model 'UserDevice'
        db.delete_table('session_userdevice')

        # Deleting model 'Session'
        db.delete_table('session_session')

        # Deleting model 'SessionValue'
        db.delete_table('session_sessionvalue')

        # Deleting model 'GTime'
        db.delete_table('session_gtime')

        # Deleting model 'GReferrerSite'
        db.delete_table('session_greferrersite')

        # Deleting model 'GReferrerKeyword'
        db.delete_table('session_greferrerkeyword')


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
        'session.greferrerkeyword': {
            'Meta': {'object_name': 'GReferrerKeyword'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiongroupbyReferrerkeyword'", 'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerKeyword'", 'null': 'True', 'to': "orm['referrer.Keyword']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'session.greferrersite': {
            'Meta': {'object_name': 'GReferrerSite'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiongroupbyReferrerSite'", 'to': "orm['project.Project']"}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerSite'", 'null': 'True', 'to': "orm['referrer.Site']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'session.gtime': {
            'Meta': {'unique_together': "(('datetype', 'dateline'),)", 'object_name': 'GTime'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiongroupbytime'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
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
        'session.sessionvalue': {
            'Meta': {'object_name': 'SessionValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value'", 'to': "orm['session.Session']"}),
            'value': ('django.db.models.fields.TextField', [], {})
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

    complete_apps = ['session']