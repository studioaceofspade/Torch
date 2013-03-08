from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from torch.account.forms import UserForm


class AccountFormTestCase(TestCase):
    def test_empty(self):
        # Build the form with no input. Equivalent to no POST vars.
        form = UserForm({})
        is_valid = form.is_valid()
        assert not is_valid
        for key in form.errors.keys():
            self.assertEqual(
                form.errors[key],
                ['This field is required.'],
            )

    def test_valid(self):
        params = {
            'username': 'username',
            'password1': 'pw',
            'password2': 'pw',
            'first_name': 'first_name',
        }
        form = UserForm(params)
        is_valid = form.is_valid()
        assert is_valid

        user = form.save()
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.first_name, 'first_name')
        assert user.check_password('pw')

    def test_invalid_password(self):
        params = {
            'username': 'username',
            'password1': 'pw',
            'password2': 'pw1',  # Different
            'first_name': 'first_name',
        }
        form = UserForm(params)
        is_valid = form.is_valid()
        assert not is_valid

        self.assertEqual(
            form.errors['password2'],
            ['The passwords must match.'],
        )
        with self.assertRaises(User.DoesNotExist):
            User.objects.get()


class AccountClientTestCase(TestCase):
    def test_create_idea(self):
        c = self.client

        create_user = reverse('account_create')
        params = {
            'username': 'username',
            'password1': 'pw',
            'password2': 'pw',
            'first_name': 'first_name',
        }
        r = c.post(create_user, params)
        self.assertEqual(r.status_code, 302)

        user = User.objects.get()
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.first_name, 'first_name')
        assert user.check_password('pw')

    def test_logged_in_user_can_create_idea(self):
        c = self.client
        c.logout()

        create_idea = reverse('idea_create')
        account_login = reverse('account_login')

        # Try to GET the create_idea page without being logged in.
        r = c.get(create_idea)
        self.assertEqual(r.status_code, 302)

        # Login and try again.
        User.objects.create_user('user', password='pw')
        params = {
            'username': 'user',
            'password': 'pw',
        }
        r = c.post(account_login, params)
        self.assertEqual(r.status_code, 302)

        # And now it works
        r = c.get(create_idea)
        self.assertEqual(r.status_code, 200)
