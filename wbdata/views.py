from django.template import RequestContext
from django.shortcuts import *
from models import *
from datetime import datetime

def country_object_default(request, country_id):
    end_year = datetime.now().year
    begin_year = end_year - 10
    country = get_object_or_404(Country, id=country_id)
    datapoints = country.datapoint_set.filter(year__range=(begin_year, end_year))
    return render_to_response('country_object_detail.html', {'country': country, 'datapoints': datapoints}, context_instance=RequestContext(request))
