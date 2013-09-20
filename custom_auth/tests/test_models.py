from django.test import TestCase

from custom_auth.models import NestedGroupManager, NestedGroup, CustomUser


class ModelTestCases(TestCase):
    def setUp(self):
        # self.adminUser = CustomUser(email='admin@example.com',
        #                             first_name='Joe',
        #                             last_name='Admin')
        self.user = CustomUser.objects.create(email='joeteacher@vashonsd.org',
                                              first_name='Joe',
                                              last_name='Teacher')
        self.highGroup = NestedGroup.objects.create(name='high')
        self.mediumGroup = NestedGroup.objects.create(name='med', parent=self.highGroup)
        self.lowGroup = NestedGroup.objects.create(name='low', parent=self.mediumGroup)
        self.otherGroup = NestedGroup.objects.create(name='outsider')
        self.groupList = [self.highGroup, self.mediumGroup, self.lowGroup]
        self.disjointList = [self.highGroup, self.mediumGroup, self.lowGroup, self.otherGroup]
        self.groupManager = NestedGroupManager()
        self.userGroupsManager = self.user.groups

    def tearDown(self):
        pass

    def test_returns_children(self):
        self.assertIn(self.lowGroup, self.groupManager.only_children_of(self.highGroup))

    def test_finds_top_group(self):
        self.assertEqual(self.groupManager.top_groups(self.groupList)[0], self.highGroup)

    def test_finds_two_top_groups(self):
        self.assertEqual(len(self.groupManager.top_groups(self.disjointList)), 2)

    def test_3_equals_3(self):
        self.assertEqual(3, 3)

    def test_add_only_adds_one_group(self):
        self.userGroupsManager.add(self.lowGroup, self.mediumGroup)
        print self.userGroupsManager.all()
        self.assertEqual(self.userGroupsManager.count(), 1)

    # def test_user_status_over_positive(self):
    #     self.

