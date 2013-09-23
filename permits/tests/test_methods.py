import pprint

from django.test import TestCase

from permits import methods as permit
from permits.configs import compile

from custom import dictdiffer as differ

pp = pprint.PrettyPrinter()


class PermitMethodTestCases(TestCase):

    def setUp(self):
        self.narrowedConfig = {
            'wat':{
                'fields': {
                    'foo': 4,
                    'bar': 5,
                    'baz': 7
                },
                'methods': {
                    'GET': 5,
                    'DELETE': 1,
                    'PUT': 0
                }
            }
        }

        self.fullConfig = {
            'fields': {
                'foo': '-640',
                'bar': 'm755'
            },
            'methods': {
                'GET': '-555',
                'PUT': '-700'
            }
        }

        self.modifier = {
            'fields': {
                'omit': ['foo'],
                'extend': ['bar']
            },
            'methods': {
                'omit': ['PUT']
            }
        },
        self.new_perms = {
                'skillsets': {
                    'fields': {'locked': '+rwx'},
                    'methods': {'PUT': '+rx'}}}

        self.testDict = {
            'skillsets': {
                'fields':
            {'title': '-660',
             'locked': '-000',
             'short_description': '-660',
             'long_description': '-640',
             'challenges': 'm755'
             },
                'methods': {
                    'PUT': '-500',
                    'GET': '-555',
                    'DELETE': '-500'
                }
            }
        }

    def test_can(self):
        result = permit.can('group', 'write', '0761')
        self.assertTrue(result)

    def test_can_via(self):
        self.parent_permissions = self.testDict['skillsets']
        self.assertTrue(
            permit.can_via('challenges',
                            'execute',
                            'group',
                            self.parent_permissions))
        self.assertFalse(
            permit.can_via('challenges',
                            'write',
                            'group',
                            self.parent_permissions))

    def test_permitted_set(self):
        self.permitted_fields = permit.permitted_set(
            self.testDict['skillsets']['fields'], 'group', 'write')
        print "\n"
        print "Sort fields by one kind of permission for a user type."
        print "(function: permitted_set(dictionary,whom,method)"
        print "Initial fields: %s" % self.testDict['skillsets']['fields']
        print "Whom: 'group'"
        print "Method: 'write'"
        print "Result: %s" % self.permitted_fields

    def test_allowed_methods_of(self):
        self.allowed_list = permit.allowed_methods_of(
            self.narrowedConfig['wat']['methods'])
        print "\n"
        print "Allowed List from Methods Fragment"
        print "Original config fragment: %s" % self.narrowedConfig['wat']['methods']
        print "Result: %s" % self.allowed_list
        self.assertIn('GET', self.allowed_list['offered'])
        self.assertNotIn('PUT', self.allowed_list['offered'])

    def test_methods_for_traversal(self):
        methods = permit.methods_for_traversal('wat','baz',self.narrowedConfig)
        print 'Result of testing methods for traversal: %s' % str(methods)
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)

    def test_traversal_bits(self):
        reduced = permit.traversal_bits(self.testDict)
        print self.assertEqual(reduced['skillsets']['fields']['challenges'], 'm')
        print self.assertEqual(reduced['skillsets']['fields']['title'], '-')

    def test_compile_changes_config(self):
        new_dict = compile.modify_config(self.testDict, self.new_perms)
        diff = differ.diff(new_dict, self.testDict)
        print '\n'
        print 'Changes in modified config: %s' % str(list(diff))
        self.assertNotEqual(diff, [])
