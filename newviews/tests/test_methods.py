import pprint

from django.test import TestCase
from django.test.client import Client, RequestFactory

from newviews import methods, helpers

from badges.models import Challenge

from build.factories import GroupFactory, UserFactory, ChallengeFactory

from permits import methods as permit

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
                        'skillset': '0755',
                        'user': '0755',
                        'group': '0755',
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

        self.tapered_config = permit.reduce_permissions_dictionary_to('group',self.challenge_config)

        self.client = Client()

        self.requestFactory = RequestFactory()

        self.group = GroupFactory.create()

        self.user = UserFactory.create()

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

    def test_sorting_of_traversals(self):
        self.traversals = helpers.valid_traversals()

    def test_posting_to_collection_with_valid_fields(self):
        print '\n'
        print 'Posting to a collection.'
        self.request = self.requestFactory.post('/skillsets/11/challenges',
                                    data={
                                        'title': 'Make a stop-motion movie',
                                        'short_description': 'A brief description',
                                        'long_description': 'A much longer description.',
                                        'sudo': 'A malicious attack!'
                                    })
        self.response = methods.post_to_collection(
            request = self.request,
            resource = 'challenges',
            config = self.challenge_config
            )
        self.form = self.response[1]['target']['form']
        pp.pprint(self.form.validate())
        pp.pprint(self.response)

    def test_get_instance(self):
        print '\n'
        print 'Getting an instance'
        pp.pprint(methods.get_instance(resource='challenges', instance=self.instance,
                                       user=None, user_role='group',
                                       config=self.challenge_config, depth=0))

    def test_get_post_form(self):
        print '\n'
        print 'Getting a post form'
        self.form_dict = methods.get_post_form(resource='challenges', config=self.challenge_config)
        pp.pprint(self.form_dict['target']['form'].as_p())
