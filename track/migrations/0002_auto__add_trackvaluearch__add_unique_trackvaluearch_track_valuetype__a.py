# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrackValueArch'
        db.create_table('track_trackvaluearch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valuetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['track.TrackValueType'], null=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='')),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['track.TrackArch'])),
        ))
        db.send_create_signal('track', ['TrackValueArch'])

        # Adding unique constraint on 'TrackValueArch', fields ['track', 'valuetype']
        db.create_unique('track_trackvaluearch', ['track_id', 'valuetype_id'])

        # Adding model 'TrackArch'
        db.create_table('track_trackarch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Action'])),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('referrer_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referrer.Site'], null=True)),
            ('referrer_keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referrer.Keyword'], null=True)),
            ('step', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=50)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=50)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['session.SessionArch'])),
            ('from_track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['track.TrackArch'], null=True)),
        ))
        db.send_create_signal('track', ['TrackArch'])


    def backwards(self, orm):
        # Removing unique constraint on 'TrackValueArch', fields ['track', 'valuetype']
        db.delete_unique('track_trackvaluearch', ['track_id', 'valuetype_id'])

        # Deleting model 'TrackValueArch'
        db.delete_table('track_trackvaluearch')

        # Deleting model 'TrackArch'
        db.delete_table('track_trackarch')


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
        'project.action': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'Action'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_flag': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action'", 'to': "orm['project.Project']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'xpath': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.UserAgent']", 'null': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.UserDevice']", 'null': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.UserOS']", 'null': 'True'}),
            'permanent_session_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['project.Project']", 'null': 'True', 'blank': 'True'}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Keyword']", 'null': 'True'}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Site']", 'null': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'user_timezone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'session.sessionarch': {
            'Meta': {'object_name': 'SessionArch'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.UserAgent']", 'null': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.UserDevice']", 'null': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.UserOS']", 'null': 'True'}),
            'permanent_session_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['project.Project']", 'null': 'True', 'blank': 'True'}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Keyword']", 'null': 'True'}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Site']", 'null': 'True'}),
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
        },
        'track.gaction': {
            'Meta': {'object_name': 'GAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyaction'", 'to': "orm['project.Action']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyaction'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'track.greferrerkeywordandaction': {
            'Meta': {'object_name': 'GReferrerKeywordAndAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerKeywordAndAction'", 'to': "orm['project.Action']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'max_length': '13'}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerKeywordAndAction'", 'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerKeywordAndAction'", 'null': 'True', 'to': "orm['referrer.Keyword']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'track.greferrersiteandaction': {
            'Meta': {'object_name': 'GReferrerSiteAndAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerSiteAndAction'", 'to': "orm['project.Action']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'max_length': '13'}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerSiteAndAction'", 'to': "orm['project.Project']"}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerSiteAndAction'", 'null': 'True', 'to': "orm['referrer.Site']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'track.gvalue': {
            'Meta': {'object_name': 'GValue'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'max_length': '13'}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyvalue'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'valuetype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gvalue'", 'null': 'True', 'to': "orm['track.TrackValueType']"})
        },
        'track.track': {
            'Meta': {'object_name': 'Track'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Action']"}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.Track']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Keyword']", 'null': 'True'}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Site']", 'null': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.Session']"}),
            'step': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '50'}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'track.trackarch': {
            'Meta': {'object_name': 'TrackArch'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Action']"}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.TrackArch']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Keyword']", 'null': 'True'}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrer.Site']", 'null': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.SessionArch']"}),
            'step': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '50'}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'track.trackvalue': {
            'Meta': {'unique_together': "(('track', 'valuetype'),)", 'object_name': 'TrackValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.Track']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'valuetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.TrackValueType']", 'null': 'True'})
        },
        'track.trackvaluearch': {
            'Meta': {'unique_together': "(('track', 'valuetype'),)", 'object_name': 'TrackValueArch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.TrackArch']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'valuetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.TrackValueType']", 'null': 'True'})
        },
        'track.trackvaluetype': {
            'Meta': {'object_name': 'TrackValueType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackvaluetype'", 'to': "orm['project.Project']"})
        }
    }

    complete_apps = ['track']