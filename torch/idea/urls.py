from django.conf.urls import patterns, url

urlpatterns = patterns(
    'torch.idea.views',
    url(r'^create/$', 'create', name='idea_create'),
    url(r'^(?P<idea_id>\d+)/view/$', 'view', name='idea_view'),
    url(r'^manage/$', 'manage', name='idea_manage'),
)
