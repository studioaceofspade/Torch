from django.contrib.auth.models import User
from django.test import TestCase

from torch.idea.models import Idea, create_idea, CREATIVITY
from torch.idea.forms import IdeaForm


class IdeaTestCase(TestCase):
    def test_simple(self):
        user = User.objects.create()
        idea = Idea.objects.create(
            author=user,
            title='test',
            description='foobar',
            tag=CREATIVITY,
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
            tag=CREATIVITY,
        )
        self.assertNotEqual(idea, None)
        self.assertEqual(idea.author, user)
        self.assertEqual(idea.title, 'test')
        self.assertEqual(idea.description, 'foobar')


class IdeaFormTestCase(TestCase):
    def test_empty(self):
        # Build the form with no input. Equivalent to no POST vars.
        form = IdeaForm({})
        is_valid = form.is_valid()
        assert not is_valid
        self.assertEqual(
            form.errors['author'],
            ['This field is required.'],
        )
        self.assertEqual(
            form.errors['title'],
            ['This field is required.'],
        )
        self.assertEqual(
            form.errors['description'],
            ['This field is required.'],
        )
        self.assertEqual(
            form.errors['tag'],
            ['This field is required.'],
        )

    def test_valid(self):
        user = User.objects.create()
        params = {
            'author': user.pk,
            'title': 'title',
            'description': 'description',
            'tag': CREATIVITY,
        }
        form = IdeaForm(params)
        is_valid = form.is_valid()
        assert is_valid

        idea = form.save()
        self.assertEqual(
            idea.author,
            user,
        )
        self.assertEqual(
            idea.title,
            'title',
        )
        self.assertEqual(
            idea.description,
            'description',
        )
        self.assertEqual(
            idea.tag,
            CREATIVITY,
        )

    def test_invalid_tag(self):
        user = User.objects.create()
        params = {
            'author': user.pk,
            'title': 'title',
            'description': 'description',
            'tag': 1000,  # Not a valid tag.
        }
        form = IdeaForm(params)
        is_valid = form.is_valid()
        assert not is_valid

        self.assertEqual(
            form.errors['tag'],
            [
                'Select a valid choice. 1000 is '
                'not one of the available choices.',
            ],
        )

    def test_invalid_user(self):
        params = {
            'author': 1,  # Not a valid user.
            'title': 'title',
            'description': 'description',
            'tag': CREATIVITY,
        }
        form = IdeaForm(params)
        is_valid = form.is_valid()
        assert not is_valid

        self.assertEqual(
            form.errors['author'],
            [
                'Select a valid choice. That choice is '
                'not one of the available choices.',
            ],
        )
