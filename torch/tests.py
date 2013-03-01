from django.test import TestCase
from django.core.urlresolvers import reverse


class BaseTestCase(TestCase):
    def test_simple(self):
        c = self.client

        home = reverse('home')
        r = c.get(home)
        self.assertEqual(r.status_code, 200)
