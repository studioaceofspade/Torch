from django.conf.urls import patterns, url

urlpatterns = patterns(
    'torch.idea.views',
    url(r'^create/$', 'create', name='idea_create'),
)
