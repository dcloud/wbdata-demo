from django.conf.urls.defaults import *
from django.conf import settings

from staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wbdata_demo/', include('wbdata_demo.foo.urls')),
    (r'^wbdata/', include('wbdata.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


# If in debug mode, we use django to serve images
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    
