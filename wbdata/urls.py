from django.conf.urls.defaults import *
from models import *

urlpatterns = patterns('wbdata.views',
    url(r'(?P<country_id>[-\w]+)/$', 'country_object_default', name='country_object_default'),
)