# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'GTime', fields ['dateline', 'datetype']
        db.delete_unique('session_gtime', ['dateline', 'datetype'])

        # Deleting field 'GReferrerKeyword.dateline'
        db.delete_column('session_greferrerkeyword', 'dateline')

        # Deleting field 'GReferrerKeyword.datetype'
        db.delete_column('session_greferrerkeyword', 'datetype')

        # Deleting field 'GTime.dateline'
        db.delete_column('session_gtime', 'dateline')

        # Deleting field 'GTime.datetype'
        db.delete_column('session_gtime', 'datetype')

        # Deleting field 'GReferrerSite.dateline'
        db.delete_column('session_greferrersite', 'dateline')

        # Deleting field 'GReferrerSite.datetype'
        db.delete_column('session_greferrersite', 'datetype')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'GReferrerKeyword.dateline'
        raise RuntimeError("Cannot reverse this migration. 'GReferrerKeyword.dateline' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'GReferrerKeyword.datetype'
        raise RuntimeError("Cannot reverse this migration. 'GReferrerKeyword.datetype' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'GTime.dateline'
        raise RuntimeError("Cannot reverse this migration. 'GTime.dateline' and its values cannot be restored.")
        # Adding field 'GTime.datetype'
        db.add_column('session_gtime', 'datetype',
                      self.gf('django.db.models.fields.CharField')(max_length=12, null=True),
                      keep_default=False)

        # Adding unique constraint on 'GTime', fields ['dateline', 'datetype']
        db.create_unique('session_gtime', ['dateline', 'datetype'])


        # User chose to not deal with backwards NULL issues for 'GReferrerSite.dateline'
        raise RuntimeError("Cannot reverse this migration. 'GReferrerSite.dateline' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'GReferrerSite.datetype'
        raise RuntimeError("Cannot reverse this migration. 'GReferrerSite.datetype' and its values cannot be restored.")

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
        'datapanel.timeline': {
            'Meta': {'unique_together': "(('datetype', 'dateline'),)", 'object_name': 'Timeline'},
            'dateline': ('django.db.models.fields.DateTimeField', [], {}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiongroupbyReferrerkeyword'", 'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerKeyword'", 'null': 'True', 'to': "orm['referrer.Keyword']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datapanel.Timeline']", 'null': 'True'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'session.greferrersite': {
            'Meta': {'object_name': 'GReferrerSite'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiongroupbyReferrerSite'", 'to': "orm['project.Project']"}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GReferrerSite'", 'null': 'True', 'to': "orm['referrer.Site']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datapanel.Timeline']", 'null': 'True'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'session.gtime': {
            'Meta': {'object_name': 'GTime'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiongroupbytime'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datapanel.Timeline']", 'null': 'True'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
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
        'session.sessionvalue': {
            'Meta': {'unique_together': "(('session', 'valuetype'),)", 'object_name': 'SessionValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.Session']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'valuetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.SessionValueType']", 'null': 'True'})
        },
        'session.sessionvaluearch': {
            'Meta': {'unique_together': "(('session', 'valuetype'),)", 'object_name': 'SessionValueArch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.SessionArch']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'valuetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['session.SessionValueType']", 'null': 'True'})
        },
        'session.sessionvaluetype': {
            'Meta': {'object_name': 'SessionValueType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessionvaluetype'", 'to': "orm['project.Project']"})
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