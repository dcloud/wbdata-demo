from django.conf.urls.defaults import *
from models import *

urlpatterns = patterns('wbdata.views',
    url(r'^$', 'countries_list', name='countries_list'),
    url(r'country/(?P<country_id>\w{3})/$', 'country_object_detail', name='country_object_detail'),
    url(r'country/(?P<country_id>\w{3})/indicator/(?P<indicator_id>[\.\w]+)/', 'country_indicator_list', name='country_indicator_list'),
    url(r'indicator/(?P<indicator_id>[\.\w]+)/$', 'indicator_object_detail', name='indicator_object_detail'),
)