from django.test import TestCase

from newviews.view_configs import mods

class ViewModsTestCases(TestCase):
    def setUp(self):
        self.modFragment = {'challenges': {
                0: {},
                1: {
                    'fields': {
                        'omit': [
                            'long_description','slug','created_at','entries','resources','tools','skillset'
                        ],
                        'extend': [
                            'resources'
                        ]
                    },
                    'methods': {
                        'omit': [
                            'PUT'
                        ]
                    }
                },
                2: {
                    'fields': {
                        'omit': [
                            'tags','short_description'
                        ]
                    },
                    'methods': {
                        'omit': [
                            'DELETE'
                        ]
                    }
                }
            }
        }

        self.config = {
            'fields': {
                'title': '0640',
                'short_description': '0640',
                'long_description': '0640',
                'slug': '0400',
                'created_at': '0000',
                'skillset': '0600',
                'entries': '0755',
                'resources': '0755',
                'tags': '0755',
                'tools': '0755'
            },
            'methods': {
                'PUT': '0700',
                'GET': '0555',
                'DELETE': '0500'
            }
        }

    def test_mod_compiler(self):
        print '\n'
        print 'Mod compiles to different levels'
        print 'Mod fragement: %s' % self.modFragment['challenges']
        print 'Compiled at level 0:'
        print mods.compile_mod_to(self.modFragment['challenges'],0)
        print 'Compiled at level 1:'
        print mods.compile_mod_to(self.modFragment['challenges'],1)
        print 'Compiled at level 2:'
        print mods.compile_mod_to(self.modFragment['challenges'],2)

    def test_filter_permissions(self):
        print '\n'
        print "A permissions fragment filtered to different depths"
        print 'Mod fragement: %s' % self.modFragment['challenges']
        print 'Original permissions dictionary: %s' % self.config
        print 'Filtered to level 0:'
        print mods.filter_permissions_for('challenges',self.config,0)
        print 'Filtered to level 1:'
        print mods.filter_permissions_for('challenges',self.config,1)
        print 'Filtered to level 2:'
        print mods.filter_permissions_for('challenges',self.config,2)