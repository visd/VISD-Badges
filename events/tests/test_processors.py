from django.test import TestCase
from django.template import Context, Template

from build import factories as corefactories
from badges.models import Challenge

from events import processors
from events.models import Event



class ProcessorTestCases(TestCase):
    def setUp(self):
        self.challenge = corefactories.ChallengeFactory(title="Blow bubbles")
        self.user = "dummyuser"
        self.event_type = "test-template"

        self.event = processors.register_event(self.event_type, self.user, self.challenge)

    def tearDown(self):
        self.challenge.delete()
        self.event.delete()

    def test_returns_new_event(self):
        self.assertIsInstance(self.event, Event)

    def test_event_relates_to_challenge(self):
        self.assertIsInstance(self.event.content_object, Challenge)

    def test_event_challenge_returns_title(self):
        self.assertEqual(self.event.content_object.title, "Blow bubbles")

    def test_event_returns_html(self):
        self.assertEqual(self.event._as_html(),"haha")