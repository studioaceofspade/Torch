from django.conf.urls import patterns, url

urlpatterns = patterns(
    'torch.account.views',
    url(
        r'^login/$',
        'account',
        kwargs={'is_create': False},
        name='account_login',
    ),
    url(
        r'^create/$',
        'account',
        kwargs={'is_create': True},
        name='account_create',
    ),
    url('^logout/$', 'logout', name='account_logout'),
    url('^(?P<user_id>\d+)/mine/$', 'my_account', name='account_my_account'),
    url(
        '^forgot_password/$',
        'forgot_password',
        kwargs={'success': False},
        name='account_forgot_password',
    ),
    url(
        '^forgot_password/success/$',
        'forgot_password',
        kwargs={'success': True},
        name='account_forgot_password_success',
    ),
)
