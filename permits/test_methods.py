from django.test import TestCase

from permits import methods

class PermitsMethodsTestCases(TestCase):
    def setUp(self):
        self.testDict = {
            'skillsets': {
                'fields':
                    {'title': '0660',
                    'short_description': '0660',
                    'long_description': '0640',
                    'challenges': '0755'
                },
                'methods': {
                    'PUT': '0500',
                    'GET': '0555',
                    'DELETE': '0500'
                }
            }
        }

    def test_can(self):
        result = methods.can('group','write','0761')
        self.assertTrue(result)

    def test_can_via(self):
        self.parent_permissions = self.testDict['skillsets']
        self.assertTrue(methods.can_via('challenges','execute','group',self.parent_permissions))
        self.assertFalse(methods.can_via('challenges','write','group',self.parent_permissions))

    def test_permitted_set(self):
        self.permitted_fields = methods.permitted_set(self.testDict['skillsets']['fields'],'group','write')
        print "\n"
        print "Sort fields by one kind of permission for a user type."
        print "(function: permitted_set(dictionary,whom,method)"
        print "Initial fields: %s" % self.testDict['skillsets']['fields']
        print "Whom: 'group'"
        print "Method: 'write'"
        print "Result: %s" % self.permitted_fields