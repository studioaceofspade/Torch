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
)
