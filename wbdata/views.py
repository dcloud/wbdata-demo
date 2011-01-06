from django.template import RequestContext
from django.shortcuts import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import *
from datetime import datetime

def country_object_default(request, country_id):
    end_year = datetime.now().year
    begin_year = end_year - 10
    country = get_object_or_404(Country, id=country_id.upper())
    datapoint_list = country.datapoint_set.filter(year__range=(begin_year, end_year)).order_by('indicator__id', '-year')
    
    paginator = Paginator(datapoint_list, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        datapoints = paginator.page(page)
    except (EmptyPage, InvalidPage):
        datapoints = paginator.page(paginator.num_pages)
    
    return render_to_response('country_object_detail.html', {'country': country, 'datapoints': datapoints}, context_instance=RequestContext(request))
