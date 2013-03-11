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
            'username': 'username@example.com',
            'password': 'pw',
            'first_name': 'first_name',
        }
        form = UserForm(params)
        is_valid = form.is_valid()
        assert is_valid

        user = form.save()
        self.assertEqual(user.username, 'username@example.com')
        self.assertEqual(user.email, 'username@example.com')
        self.assertEqual(user.first_name, 'first_name')
        assert user.check_password('pw')


class AccountClientTestCase(TestCase):
    def test_create_idea(self):
        c = self.client

        create_user = reverse('account_create')
        params = {
            'username': 'username@example.com',
            'password': 'pw',
            'first_name': 'first_name',
        }
        r = c.post(create_user, params)
        self.assertEqual(r.status_code, 302)

        user = User.objects.get()
        self.assertEqual(user.username, 'username@example.com')
        self.assertEqual(user.email, 'username@example.com')
        self.assertEqual(user.first_name, 'first_name')
        assert user.check_password('pw')

    def test_login_login_my_account(self):
        c = self.client

        account_login = reverse('account_login')
        r = c.get(account_login)

        self.assertNotContains(r, 'my account')
        self.assertNotContains(r, 'logout')
        self.assertContains(r, '>login<')

        # Login and try again.
        User.objects.create_user('user', password='pw')
        params = {
            'username': 'user',
            'password': 'pw',
        }
        r = c.post(account_login, params)
        self.assertEqual(r.status_code, 302)

        r = c.get(account_login)
        self.assertContains(r, 'my account')
        self.assertContains(r, 'logout')
        self.assertNotContains(r, '>login<')

    def test_logout(self):
        c = self.client

        account_logout = reverse('account_logout')
        account_login = reverse('account_login')

        User.objects.create_user('user', password='pw')
        assert c.login(username='user', password='pw')

        r = c.get(account_logout)
        self.assertRedirects(r, account_login)

        r = c.get(account_login)
        self.assertNotContains(r, 'my account')

    def test_account_edit_all_blank(self):
        c = self.client

        user = User.objects.create(
            username='username@username.com',
            first_name='first_name',
        )
        user.set_password('pw')
        user.save()
        assert c.login(username='username@username.com', password='pw')
        my_account = reverse(
            'account_my_account',
            kwargs={
                'user_id': user.pk,
            },
        )
        params = {
            'username': '',
            'first_name': '',
            'password': '',
            'password1': '',
        }

        r = c.post(my_account, params)
        self.assertEqual(r.status_code, 302)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.username, 'username@username.com')
        self.assertEqual(user.email, 'username@username.com')
        self.assertEqual(user.first_name, 'first_name')

    def test_account_edit_change_username(self):
        c = self.client

        user = User.objects.create(
            username='username@username.com',
            first_name='first_name',
        )
        user.set_password('pw')
        user.save()
        assert c.login(username='username@username.com', password='pw')
        my_account = reverse(
            'account_my_account',
            kwargs={
                'user_id': user.pk,
            },
        )
        params = {
            'username': 'test@test.com',
            'first_name': '',
            'password': '',
            'password1': '',
        }

        r = c.post(my_account, params)
        self.assertEqual(r.status_code, 302)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.username, 'test@test.com')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.first_name, 'first_name')

    def test_account_edit_change_first_name(self):
        c = self.client

        user = User.objects.create(
            username='username@username.com',
            first_name='first_name',
        )
        user.set_password('pw')
        user.save()
        assert c.login(username='username@username.com', password='pw')
        my_account = reverse(
            'account_my_account',
            kwargs={
                'user_id': user.pk,
            },
        )
        params = {
            'username': '',
            'first_name': 'last_name',
            'password': '',
            'password1': '',
        }

        r = c.post(my_account, params)
        self.assertEqual(r.status_code, 302)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.username, 'username@username.com')
        self.assertEqual(user.email, 'username@username.com')
        self.assertEqual(user.first_name, 'last_name')

    def test_account_edit_change_password(self):
        c = self.client

        user = User.objects.create(
            username='username@username.com',
            first_name='first_name',
        )
        user.set_password('pw')
        user.save()
        assert c.login(username='username@username.com', password='pw')
        my_account = reverse(
            'account_my_account',
            kwargs={
                'user_id': user.pk,
            },
        )
        params = {
            'username': '',
            'first_name': '',
            'password': 'pw',
            'password1': 'pw',
        }

        r = c.post(my_account, params)
        self.assertEqual(r.status_code, 302)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.username, 'username@username.com')
        self.assertEqual(user.email, 'username@username.com')
        self.assertEqual(user.first_name, 'first_name')
        assert user.check_password('pw')

    def test_account_edit_invalid_password(self):
        c = self.client

        user = User.objects.create(
            username='username@username.com',
            first_name='first_name',
        )
        user.set_password('password')
        user.save()
        assert c.login(username='username@username.com', password='password')
        my_account = reverse(
            'account_my_account',
            kwargs={
                'user_id': user.pk,
            },
        )
        params = {
            'username': '',
            'first_name': '',
            'password': 'pw',
            'password1': 'pw1',
        }

        r = c.post(my_account, params)
        self.assertEqual(r.status_code, 200)
        self.assertFormError(
            r,
            'form',
            'password',
            'The two passwords did not match.',
        )

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.username, 'username@username.com')
        self.assertEqual(user.first_name, 'first_name')
        assert user.check_password('password')

    def test_account_edit_ensure_only_current_user(self):
        c = self.client

        user = User.objects.create(
            username='username@username.com',
            first_name='first_name',
        )
        my_account = reverse(
            'account_my_account',
            kwargs={
                'user_id': user.pk,
            },
        )
        logged_in_user = User.objects.create(
            username='logged_in_user',
        )
        logged_in_user.set_password('pw')
        logged_in_user.save()

        assert c.login(username='logged_in_user', password='pw')

        r = c.get(my_account)
        self.assertEqual(r.status_code, 404)
