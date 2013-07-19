# from django.test import TestCase
# from django.template import Template

# from events import models as eventmodels
# from badges import models as coremodels

# from build import factories

# class EventTypeTestCases(TestCase):
#     def setUp(self):
#         self.event_type = eventfactories.EventTypeFactory()

#     def test_eventtype_is_an_eventtype(self):
#         self.assertIsInstance(self.event_type, eventmodels.EventType)

#     def test_event_type_returns_template(self):
#         self.assertIsInstance(self.event_type.get_template(), Template)

#     def tearDown(self):
#         self.event_type.delete()