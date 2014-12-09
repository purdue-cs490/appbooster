from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('application.views',
    # Examples:
    # url(r'^$', 'appbooster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^create/$', 'create', name='application_create'),
    url(r'^(?P<pk>[0-9]+)/$', 'app', name='application_app'),
    url(r'^(?P<pk>[0-9]+)/delete$', 'delete', name='application_delete'),
    url(r'^private/deploy/$', 'deploy_app', name='application_deploy'),
)
