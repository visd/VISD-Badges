import pprint

from django.test import TestCase

from newviews import methods

from badges.models import Challenge

from build.factories import ChallengeFactory

pp = pprint.PrettyPrinter()

class ViewMethodTestCases(TestCase):
    def setUp(self):
        self.narrowedConfig = {
            'fields':{
                'foo':4,
                'bar':5
            },
            'methods':{
                'GET':5,
                'PUT':0
            }
        }
        self.fullConfig = {
            'fields':{
                'foo':'0640',
                'bar':'0755'
            },
            'methods':{
                'GET':'0555',
                'PUT':'0700'
            }
        }
        self.modifier = {
            'fields': {
                'omit':['foo'],
                'extend':['bar']
            },
            'methods': {
                'omit': ['PUT']
            }
        }
        self.challenge_config = {
            'challenges': {
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
            }
        self.instance = ChallengeFactory.create()


    def test_condition_view_removes_fields(self):
        self.modified = methods.condition_view(self.fullConfig,self.modifier)
        self.assertIn('bar',self.modified['fields'])
        self.assertIn('GET',self.modified['methods'])
        self.assertNotIn('foo',self.modified['fields'])
        self.assertNotIn('PUT',self.modified['methods'])
        print '\n'
        print 'Conditioning View Removes Fields'
        print "Original config: %s" % self.fullConfig
        print "Modifier: %s" % self.modifier
        print "Result: %s" % self.modified

    def test_sorted_fields_of(self):
        self.sorted_config = methods.sorted_fields_of(self.narrowedConfig['fields'])
        print "\n"
        print "Fields Sorted into Fields and Traversals"
        print "Narrowed config: %s" % self.narrowedConfig['fields']
        print "Becomes: %s" % self.sorted_config
        self.assertIn('foo', self.sorted_config['fields']['read'])

    def test_allowed_methods_of(self):
        self.allowed_list = methods.allowed_methods_of(self.narrowedConfig['methods'])
        print "\n"
        print "Allowed List from Methods Fragment"
        print "Original config fragment: %s" % self.narrowedConfig['methods']
        print "Result: %s" % self.allowed_list
        self.assertIn('GET',self.allowed_list['offered'])

    def test_viewmap_of(self):
        self.viewmap = methods.viewmap_of(self.narrowedConfig)
        print '\n'
        print 'Viewmap from Narrowed Config'
        print "Original config: %s" % self.narrowedConfig
        print "Result: %s" % self.viewmap

    def test_get_instance(self):
        print '\n'
        print 'Getting an instance'
        pp.pprint(methods.get_instance(resource='challenges', instance=self.instance,
                                       user=None, user_role='group',
                                       config=self.challenge_config, depth=0))
