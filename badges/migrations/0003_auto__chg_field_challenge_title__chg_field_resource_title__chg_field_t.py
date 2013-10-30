# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Challenge.title'
        db.alter_column(u'badges_challenge', 'title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256))

        # Changing field 'Resource.title'
        db.alter_column(u'badges_resource', 'title', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'Tool.title'
        db.alter_column(u'badges_tool', 'title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256))

        # Changing field 'Entry.title'
        db.alter_column(u'badges_entry', 'title', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'Skillset.title'
        db.alter_column(u'badges_skillset', 'title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256))

    def backwards(self, orm):

        # Changing field 'Challenge.title'
        db.alter_column(u'badges_challenge', 'title', self.gf('django.db.models.fields.CharField')(max_length=90, unique=True))

        # Changing field 'Resource.title'
        db.alter_column(u'badges_resource', 'title', self.gf('django.db.models.fields.CharField')(max_length=90))

        # Changing field 'Tool.title'
        db.alter_column(u'badges_tool', 'title', self.gf('django.db.models.fields.CharField')(max_length=60, unique=True))

        # Changing field 'Entry.title'
        db.alter_column(u'badges_entry', 'title', self.gf('django.db.models.fields.CharField')(max_length=120))

        # Changing field 'Skillset.title'
        db.alter_column(u'badges_skillset', 'title', self.gf('django.db.models.fields.CharField')(max_length=60, unique=True))

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
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'}),
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