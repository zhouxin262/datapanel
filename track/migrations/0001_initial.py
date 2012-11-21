# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Track'
        db.create_table('track_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='track', to=orm['project.Project'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='track', to=orm['session.Session'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='track', to=orm['project.Action'])),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('from_track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['track.Track'], null=True)),
            ('step', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=50)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=50)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('track', ['Track'])

        # Adding model 'TrackValue'
        db.create_table('track_trackvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='value', to=orm['track.Track'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('track', ['TrackValue'])

        # Adding unique constraint on 'TrackValue', fields ['track', 'name']
        db.create_unique('track_trackvalue', ['track_id', 'name'])

        # Adding model 'GAction'
        db.create_table('track_gaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyaction', to=orm['project.Project'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyaction', to=orm['project.Action'])),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('track', ['GAction'])

        # Adding model 'GValue'
        db.create_table('track_gvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyvalue', to=orm['project.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')(max_length=13)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('track', ['GValue'])

        # Adding model 'GReferrerSiteAndAction'
        db.create_table('track_greferrersiteandaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyReferrerSiteandaction', to=orm['project.Project'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyReferrersiteandaction', to=orm['project.Action'])),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')(max_length=13)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('track', ['GReferrerSiteAndAction'])

        # Adding model 'GReferrerKeywordAndAction'
        db.create_table('track_greferrerkeywordandaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyReferrerkeywordandaction', to=orm['project.Project'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trackgroupbyReferrerkeywordandaction', to=orm['project.Action'])),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('datetype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dateline', self.gf('django.db.models.fields.DateTimeField')(max_length=13)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timelength', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('track', ['GReferrerKeywordAndAction'])


    def backwards(self, orm):
        # Removing unique constraint on 'TrackValue', fields ['track', 'name']
        db.delete_unique('track_trackvalue', ['track_id', 'name'])

        # Deleting model 'Track'
        db.delete_table('track_track')

        # Deleting model 'TrackValue'
        db.delete_table('track_trackvalue')

        # Deleting model 'GAction'
        db.delete_table('track_gaction')

        # Deleting model 'GValue'
        db.delete_table('track_gvalue')

        # Deleting model 'GReferrerSiteAndAction'
        db.delete_table('track_greferrersiteandaction')

        # Deleting model 'GReferrerKeywordAndAction'
        db.delete_table('track_greferrerkeywordandaction')


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
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['session.UserAgent']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['session.UserDevice']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['session.UserOS']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'to': "orm['project.Project']"}),
            'referrer_keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['referrer.Keyword']"}),
            'referrer_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'to': "orm['referrer.Site']"}),
            'sn': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'track_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'user_language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'user_referrer': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyReferrerkeywordandaction'", 'to': "orm['project.Action']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'max_length': '13'}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyReferrerkeywordandaction'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'track.greferrersiteandaction': {
            'Meta': {'object_name': 'GReferrerSiteAndAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyReferrersiteandaction'", 'to': "orm['project.Action']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'max_length': '13'}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyReferrerSiteandaction'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'track.gvalue': {
            'Meta': {'object_name': 'GValue'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'max_length': '13'}),
            'datetype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trackgroupbyvalue'", 'to': "orm['project.Project']"}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'track.track': {
            'Meta': {'object_name': 'Track'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'track'", 'to': "orm['project.Action']"}),
            'dateline': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['track.Track']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'track'", 'to': "orm['project.Project']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'track'", 'to': "orm['session.Session']"}),
            'step': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '50'}),
            'timelength': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'track.trackvalue': {
            'Meta': {'unique_together': "(('track', 'name'),)", 'object_name': 'TrackValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value'", 'to': "orm['track.Track']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['track']