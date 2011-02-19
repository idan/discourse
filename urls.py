from django.conf.urls.defaults import *
from staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^discourse/', include('discourse.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'groups.views.index', name='desourse_index'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
