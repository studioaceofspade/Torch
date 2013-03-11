from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'torch.views.home', name='home'),
    url(r'^about/$', 'torch.views.about', name='about'),
    url(r'^contact/$', 'torch.views.contact', name='contact'),
    url(r'^idea/', include('torch.idea.urls')),
    url(r'^accounts/', include('torch.account.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
