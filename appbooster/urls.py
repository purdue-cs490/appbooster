from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('appbooster.views',
    # Examples:
    # url(r'^$', 'appbooster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'index', 
        name = 'index'),
    url(r'^dashboard/$', 'dashboard', 
        name = 'dashboard'),
    url(r'^contact/$', 'contact', 
        name = 'contact'),
    url(r'^login/$', 'login', 
        name = 'login'),
    url(r'^register/$', 'register', 
        name = 'register'),
    url(r'^logout/$', 'logout', 
        name = 'logout'),
    url(r'^profile/$', 'profile', 
        name = 'profile'),
    url(r'^not_completed/$', 'not_completed', 
        name = 'not_completed'),
    url(r'^verify/(?P<verifycode>\w+)/$', 'verify', 
        name = 'verify'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('application.urls')),
)
