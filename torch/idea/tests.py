from django.contrib.auth.models import User
from django.test import TestCase

from torch.idea.models import Idea, create_idea


class IdeaTestCase(TestCase):
    def test_simple(self):
        user = User.objects.create()
        idea = Idea.objects.create(
            author=user,
            title='test',
            description='foobar',
        )
        self.assertNotEqual(idea, None)

    def test_create_idea(self):
        # We will be using the create_idea function to create idea objects, so
        # I only ever have to change it in one place.
        user = User.objects.create()
        idea = create_idea(
            user=user,
            title='test',
            description='foobar',
        )
        self.assertNotEqual(idea, None)
        self.assertEqual(idea.author, user)
        self.assertEqual(idea.title, 'test')
        self.assertEqual(idea.description, 'foobar')
