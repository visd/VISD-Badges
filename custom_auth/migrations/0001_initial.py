# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomUser'
        db.create_table(u'custom_auth_customuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users', null=True, to=orm['custom_auth.NestedGroup'])),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=60, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'custom_auth', ['CustomUser'])

        # Adding M2M table for field memberships on 'CustomUser'
        m2m_table_name = db.shorten_name(u'custom_auth_customuser_memberships')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'custom_auth.customuser'], null=False)),
            ('nestedgroup', models.ForeignKey(orm[u'custom_auth.nestedgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customuser_id', 'nestedgroup_id'])

        # Adding model 'NestedGroup'
        db.create_table(u'custom_auth_nestedgroup', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['custom_auth.NestedGroup'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups', null=True, to=orm['custom_auth.CustomUser'])),
        ))
        db.send_create_signal(u'custom_auth', ['NestedGroup'])


    def backwards(self, orm):
        # Deleting model 'CustomUser'
        db.delete_table(u'custom_auth_customuser')

        # Removing M2M table for field memberships on 'CustomUser'
        db.delete_table(db.shorten_name(u'custom_auth_customuser_memberships'))

        # Deleting model 'NestedGroup'
        db.delete_table(u'custom_auth_nestedgroup')


    models = {
        u'custom_auth.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'null': 'True', 'to': u"orm['custom_auth.NestedGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'memberships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'members'", 'symmetrical': 'False', 'to': u"orm['custom_auth.NestedGroup']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'custom_auth.nestedgroup': {
            'Meta': {'object_name': 'NestedGroup'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['custom_auth.NestedGroup']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'null': 'True', 'to': u"orm['custom_auth.CustomUser']"})
        }
    }

    complete_apps = ['custom_auth']