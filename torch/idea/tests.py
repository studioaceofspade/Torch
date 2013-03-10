from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.simplejson import loads

from torch.idea.models import Idea, create_idea, CREATIVITY, order_by_popular
from torch.idea.forms import make_IdeaForm
from torch.vote.models import Vote


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

    def test_order_by_popular(self):
        user = User.objects.create()
        idea1 = Idea.objects.create(
            author=user,
            tag=CREATIVITY,
        )
        idea2 = Idea.objects.create(
            author=user,
            tag=CREATIVITY,
        )
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        idea1.created = yesterday
        idea1.save()

        Vote.objects.create(
            voter=user,
            idea=idea1,
        )

        self.assertEqual(
            order_by_popular(Idea.objects.all()),
            [idea1, idea2],
        )

        # Now add one vote to the newer one and watch the order change.
        Vote.objects.create(
            voter=User.objects.create(username='1'),
            idea=idea2,
        )

        self.assertEqual(
            order_by_popular(Idea.objects.all()),
            [idea2, idea1],
        )


class IdeaFormTestCase(TestCase):
    def test_empty(self):
        # Build the form with no input. Equivalent to no POST vars.
        IdeaForm = make_IdeaForm(None)
        form = IdeaForm({})
        is_valid = form.is_valid()
        assert not is_valid
        for key in form.errors.keys():
            self.assertEqual(
                form.errors[key],
                ['This field is required.'],
            )

    def test_valid(self):
        user = User.objects.create()
        IdeaForm = make_IdeaForm(user)
        params = {
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
            'title': 'title',
            'description': 'description',
            'tag': 1000,  # Not a valid tag.
        }
        IdeaForm = make_IdeaForm(user)
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
            'title': 'title',
            'description': 'description',
            'tag': CREATIVITY,
        }
        IdeaForm = make_IdeaForm(None)
        form = IdeaForm(params)
        is_valid = form.is_valid()
        assert not is_valid

        self.assertEqual(
            form.errors['__all__'],
            ['This field is required.'],
        )


class IdeaClientTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('user', password='userpw')
        assert self.client.login(username='user', password='userpw')

    def _create_idea(self):
        create_idea = reverse('idea_create')
        params = {
            'title': 'title',
            'description': 'description',
            'tag': CREATIVITY,
        }
        r = self.client.post(create_idea, params)
        response = loads(r.content)
        assert 'url' in response

    def test_create_idea(self):
        self._create_idea()

        idea = Idea.objects.get()
        self.assertEqual(idea.title, 'title')
        self.assertEqual(idea.description, 'description')
        self.assertEqual(idea.author, self.user)

    def test_view_idea(self):
        c = self.client

        TITLE = 'Title of the idea'
        DESCRIPTION = 'Description of the idea'
        idea = create_idea(
            user=self.user,
            title=TITLE,
            description=DESCRIPTION,
            tag=CREATIVITY,
        )

        view_idea = reverse('idea_view', kwargs={'idea_id': idea.pk})
        with self.assertNumQueries(3):
            r = c.get(view_idea)

        self.assertContains(r, TITLE)
        self.assertContains(r, DESCRIPTION)
        self.assertContains(r, idea.get_tag_display().lower())

    def test_manage_pagination(self):
        c = self.client

        idea_manage = reverse('idea_manage')
        for _ in range(3):
            self._create_idea()

        with self.settings(TORCH_PAGINATION=1):
            r = c.get(idea_manage)
            self.assertContains(r, '>Next<')
            self.assertNotContains(r, '>Previous<')

        with self.settings(TORCH_PAGINATION=1):
            r = c.get(idea_manage + '?page=2')
            self.assertContains(r, '>Next<')
            self.assertContains(r, '>Previous<')

        with self.settings(TORCH_PAGINATION=1):
            r = c.get(idea_manage + '?page=3')
            self.assertNotContains(r, '>Next<')
            self.assertContains(r, '>Previous<')

        # Normal pagination is set to 10
        r = c.get(idea_manage)
        self.assertNotContains(r, '>Next<')
        self.assertNotContains(r, '>Previous<')

    def test_idea_manage_base(self):
        c = self.client

        idea_manage = reverse('idea_manage')
        for _ in range(3):
            self._create_idea()

        idea_manage = reverse('idea_manage')

        r = c.get(idea_manage)
        self.assertContains(r, '<tr class="idea-data"', 3)

    def test_create_idea_not_logged_in(self):
        c = self.client

        idea_create = reverse('idea_create')

        # Make sure there are no ideas and the user is not logged in.
        self.assertEqual(Idea.objects.count(), 0)
        c.logout()

        params = {
            'title': 'title',
            'description': 'description',
            'tag': CREATIVITY,
            'username': 'user',
            'password': 'userpw',
        }

        r = c.post(idea_create, params)
        response = loads(r.content)
        assert 'url' in response

        # Make sure the idea was created and that the user is logged in.
        idea = Idea.objects.get()
        self.assertEqual(idea.author, self.user)
        self.assertEqual(idea.title, 'title')
        self.assertEqual(idea.description, 'description')
        self.assertEqual(idea.tag, CREATIVITY)

        r = c.get(idea_create)
        self.assertContains(r, '>logout<')

    def test_create_idea_not_registered(self):
        c = self.client

        idea_create = reverse('idea_create')

        # Make sure there are no ideas and the user is not logged in.
        self.assertEqual(Idea.objects.count(), 0)
        c.logout()
        self.assertEqual(
            User.objects.filter(username='user@example.com').count(),
            0,
        )

        params = {
            'title': 'title',
            'description': 'description',
            'tag': CREATIVITY,
            'first_name': 'User',
            'username': 'user@example.com',
            'password': 'userpw',
        }

        r = c.post(idea_create, params)
        response = loads(r.content)
        assert 'url' in response

        # Make sure the idea was created and that the user is logged in.
        idea = Idea.objects.get()
        user = User.objects.get(username='user@example.com')
        self.assertEqual(idea.author, user)
        self.assertEqual(idea.title, 'title')
        self.assertEqual(idea.description, 'description')
        self.assertEqual(idea.tag, CREATIVITY)

        r = c.get(idea_create)
        print r.content
        self.assertContains(r, '>logout<')
