from django.conf.urls import patterns, url

urlpatterns = patterns(
    'torch.account.views',
    url(r'^login/$', 'login', name='account_login'),
)
