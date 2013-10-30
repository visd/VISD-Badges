# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'badges_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['custom_auth.CustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['custom_auth.NestedGroup'])),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'badges', ['Tag'])

        # Adding model 'Tool'
        db.create_table(u'badges_tool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tools', to=orm['custom_auth.CustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tools', to=orm['custom_auth.NestedGroup'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('url_link', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('url_title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'badges', ['Tool'])

        # Adding model 'Entry'
        db.create_table(u'badges_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['custom_auth.CustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['custom_auth.NestedGroup'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('url_link', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('url_title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['badges.Challenge'])),
        ))
        db.send_create_signal(u'badges', ['Entry'])

        # Adding M2M table for field tags on 'Entry'
        m2m_table_name = db.shorten_name(u'badges_entry_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm[u'badges.entry'], null=False)),
            ('tag', models.ForeignKey(orm[u'badges.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['entry_id', 'tag_id'])

        # Adding M2M table for field tools on 'Entry'
        m2m_table_name = db.shorten_name(u'badges_entry_tools')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm[u'badges.entry'], null=False)),
            ('tool', models.ForeignKey(orm[u'badges.tool'], null=False))
        ))
        db.create_unique(m2m_table_name, ['entry_id', 'tool_id'])

        # Adding model 'Challenge'
        db.create_table(u'badges_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges', to=orm['custom_auth.CustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges', to=orm['custom_auth.NestedGroup'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('skillset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges', to=orm['badges.Skillset'])),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('long_description', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'badges', ['Challenge'])

        # Adding M2M table for field tags on 'Challenge'
        m2m_table_name = db.shorten_name(u'badges_challenge_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm[u'badges.challenge'], null=False)),
            ('tag', models.ForeignKey(orm[u'badges.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['challenge_id', 'tag_id'])

        # Adding M2M table for field tools on 'Challenge'
        m2m_table_name = db.shorten_name(u'badges_challenge_tools')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm[u'badges.challenge'], null=False)),
            ('tool', models.ForeignKey(orm[u'badges.tool'], null=False))
        ))
        db.create_unique(m2m_table_name, ['challenge_id', 'tool_id'])

        # Adding model 'Resource'
        db.create_table(u'badges_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resources', to=orm['custom_auth.CustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resources', to=orm['custom_auth.NestedGroup'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('url_link', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('url_title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('thumb', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resources', to=orm['badges.Challenge'])),
        ))
        db.send_create_signal(u'badges', ['Resource'])

        # Adding model 'Skillset'
        db.create_table(u'badges_skillset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skillsets', to=orm['custom_auth.CustomUser'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skillsets', to=orm['custom_auth.NestedGroup'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('long_description', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'badges', ['Skillset'])

        # Adding M2M table for field tags on 'Skillset'
        m2m_table_name = db.shorten_name(u'badges_skillset_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skillset', models.ForeignKey(orm[u'badges.skillset'], null=False)),
            ('tag', models.ForeignKey(orm[u'badges.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['skillset_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'badges_tag')

        # Deleting model 'Tool'
        db.delete_table(u'badges_tool')

        # Deleting model 'Entry'
        db.delete_table(u'badges_entry')

        # Removing M2M table for field tags on 'Entry'
        db.delete_table(db.shorten_name(u'badges_entry_tags'))

        # Removing M2M table for field tools on 'Entry'
        db.delete_table(db.shorten_name(u'badges_entry_tools'))

        # Deleting model 'Challenge'
        db.delete_table(u'badges_challenge')

        # Removing M2M table for field tags on 'Challenge'
        db.delete_table(db.shorten_name(u'badges_challenge_tags'))

        # Removing M2M table for field tools on 'Challenge'
        db.delete_table(db.shorten_name(u'badges_challenge_tools'))

        # Deleting model 'Resource'
        db.delete_table(u'badges_resource')

        # Deleting model 'Skillset'
        db.delete_table(u'badges_skillset')

        # Removing M2M table for field tags on 'Skillset'
        db.delete_table(db.shorten_name(u'badges_skillset_tags'))


    models = {
        u'badges.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges'", 'to': u"orm['custom_auth.NestedGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'skillset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges'", 'to': u"orm['badges.Skillset']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'challenges'", 'symmetrical': 'False', 'to': u"orm['badges.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'tools': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'challenges'", 'symmetrical': 'False', 'to': u"orm['badges.Tool']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges'", 'to': u"orm['custom_auth.CustomUser']"})
        },
        u'badges.entry': {
            'Meta': {'object_name': 'Entry'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['badges.Challenge']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['custom_auth.NestedGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entries'", 'symmetrical': 'False', 'to': u"orm['badges.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'tools': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entries'", 'symmetrical': 'False', 'to': u"orm['badges.Tool']"}),
            'url_link': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'url_title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['custom_auth.CustomUser']"})
        },
        u'badges.resource': {
            'Meta': {'object_name': 'Resource'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': u"orm['badges.Challenge']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': u"orm['custom_auth.NestedGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumb': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'url_link': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'url_title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resources'", 'to': u"orm['custom_auth.CustomUser']"})
        },
        u'badges.skillset': {
            'Meta': {'object_name': 'Skillset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skillsets'", 'to': u"orm['custom_auth.NestedGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'skillsets'", 'symmetrical': 'False', 'to': u"orm['badges.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skillsets'", 'to': u"orm['custom_auth.CustomUser']"})
        },
        u'badges.tag': {
            'Meta': {'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': u"orm['custom_auth.NestedGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': u"orm['custom_auth.CustomUser']"}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        u'badges.tool': {
            'Meta': {'object_name': 'Tool'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tools'", 'to': u"orm['custom_auth.NestedGroup']"}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'url_link': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'url_title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tools'", 'to': u"orm['custom_auth.CustomUser']"})
        },
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

    complete_apps = ['badges']